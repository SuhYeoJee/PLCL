from collections import defaultdict
import time
import serial
from os.path import exists
from os import makedirs
import tkinter as tk
import serial.tools.list_ports

DEBUG = True
# DEBUG = False

# ===========================================================================================
class PLCReader:
    def __init__(self,ser):
        self.stationNo = b'01' #국번(gukbun)
        self.ser = ser
        self.PLCAddr = {
            'PrgNo':      'D131',
            'BondName':   'D132',
            'LotNo':      'D140',
            'RPM':        'D120',
            'TimeSet':    'D122',
            'TimeAct':    'D220',
            }
        self.PLCDataName= list(self.PLCAddr.keys())      
        self.PLCAddrSize = defaultdict(lambda:1, { # word length: DEFAULT 1W
            'BondName':   8, # BondName: 8W
            'LotNo':      5, # LotNo:5W
            })
    # -------------------------------------------------------------------------------------------
    def getIsRunning(self) -> bool:
        return self.getPLCRecv('isRunning')
    # --------------------------
    def getResList(self) -> str:
        resList = []
        for dataName in self.PLCDataName:
            res = self.getPLCRecv(dataName)
            resList.append(res)
            print(dataName + ': ' + res)
        return resList        
    # -------------------------------------------------------------------------------------------
    def MakeReadCmd(self, dataName:str) -> str:
        readAddrStr = self.PLCAddr[dataName]
        readAddrByte = b'%' + readAddrStr[0].encode('ascii') + b'W' + readAddrStr[1:].encode('ascii')
        wordLength = self.PLCAddrSize[dataName]
        wordLengthByte = (hex(wordLength)).replace('0x','').replace('0X','').zfill(2).encode('ascii')

        if wordLength == 1: readCmd = b'RSS0106' + readAddrByte # RSS
        else: readCmd = b'RSB06' + readAddrByte + wordLengthByte # RSB
        return b'\x05' + self.stationNo + readCmd + b'\x04'
    # -------------------------------------------------------------------------------------------
    def getPLCRecv(self, dataName:str=None):
        if DEBUG:
            if dataName=='isRunning': return True
            if int(time.mktime(time.localtime())) % 2:
                recv = b'\x0601RSB010244413243003500000000\x03'
            else:
                recv = b'\x0601RSS0102000A\x03'
        else:
            self.ser.write(self.MakeReadCmd(dataName))
            recv = self.ser.readline() # ex) recv = b'\x0601RSS0102000A\x03'            
    # --------------------------
        def decodeResult() -> str:
            recvStr = recv.decode('ascii')
            resultStr = ''        
            if recv[1:3] != self.stationNo: 
                ...
            elif recvStr.startswith('\x06'): # ACK
                if recvStr[3:6] == 'RSS':
                    resultStr = str(int(recvStr[10:-1],16))
                elif recvStr[3:6] == 'RSB':
                    hexStr = recvStr[10:-1]
                    resultStr = ''.join([chr(int(hexStr[i+2:i+4], 16))+chr(int(hexStr[i:i+2], 16)) for i in range(0, len(hexStr), 4)])
                else: # not read result
                    ... # print err
            else: # not ACK
                ... # print err
            return resultStr.replace('\x00','').strip()
        return decodeResult()

# ===========================================================================================


class MonitorWindow:
    def __init__(self,reader:PLCReader):
        self.reader = reader
        self.window = tk.Tk()
        self.window.title("MixerMonitor")
        self.window.geometry("400x300")
        self.entryList = self.setWindow()
        self.running = False
        # --------------------------
        self.update()
        self.window.mainloop()
    # -------------------------------------------------------------------------------------------
    def setWindow(self):
        entryList = []
        for idx,dataName in enumerate(['현재시간']+self.reader.PLCDataName):
            label = tk.Label(self.window, text=dataName)
            label.grid(row=idx, column=0, padx=5, pady=5)

            entry = tk.Entry(self.window)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entryList.append(entry)
        return entryList
    # -------------------------------------------------------------------------------------------
    def startUpdate(self):
        self.running = True

    def stopUpdate(self):
        self.running = False

    def updateEntries(self, resList):
        nowStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        for entry, res in zip(self.entryList, [nowStr]+resList):
            entry.delete(0, tk.END)
            entry.insert(0, res)

    def update(self):
        if self.running:
            resList = self.reader.getResList()
            self.updateEntries(resList)
            self.writeText(resList) # write every res
        self.running = self.reader.getIsRunning()
        self.window.after(1000, self.update)

    def writeText(self, resList):
        fileHeader = ['시간','프로그램번호','Bond명','Lot번호','RPM','설정시간','동작시간']
        resFileName = time.strftime("./output/%Y_%m_%d.txt", time.localtime())
        nowStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if not exists(resFileName):
            makedirs('./output', exist_ok=True)
            with open(resFileName, 'w') as f: 
                f.write('\t'.join(fileHeader) + '\n')
        with open(resFileName, 'a') as f: 
            f.write('\t'.join([nowStr]+resList) + '\n')
        return

# ===========================================================================================
PLC_DATA = ['PrgNo','BondName','LotNo','RPM','TimeSet','TimeAct']
# -------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # how to find port ?
    # ser = serial.Serial('COM5',115200,timeout=1)
    ports = serial.tools.list_ports.comports()
    for port_info in ports:
        print(f" - Device Name: {port_info.device}")
        print(f"   Serial Number: {port_info.serial_number}")
        print(f"   Vendor ID: {port_info.vid}")
        print(f"   Product ID: {port_info.pid}")
        print(f"   Description: {port_info.description}")
        print("\n")
    reader = PLCReader(None)
    mw = MonitorWindow(reader)
# ===========================================================================================
