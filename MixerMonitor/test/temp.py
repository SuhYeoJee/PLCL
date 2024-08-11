from collections import defaultdict
import time
import serial
from os.path import exists
from os import makedirs
import tkinter as tk

STATION_NO = b'01' #국번(gukbun)
DEBUG = True
# DEBUG = False
# -------------------------------------------------------------------------------------------
def getPLCReadCmd():
    # data addr
    PLC_ADDR = {
        'PrgNo':      'D131',
        'BondName':   'D132',
        'LotNo':      'D140',
        'RPM':        'D120',
        'TimeSet':    'D122',
        'TimeAct':    'D220',
        }
    # word length (BondName: 8W, LotNo:5W) , DEFAULT 1W
    PLC_ADDR_SIZE = defaultdict(lambda:1, {  
        'BondName':   8,
        'LotNo':      5,
        })
    # --------------------------
    def MakeReadCmd(dataName:str) -> str:
        readAddrStr = PLC_ADDR[dataName]
        readAddrByte = b'%' + readAddrStr[0].encode('ascii') + b'W' + readAddrStr[1:].encode('ascii')
        wordLength = PLC_ADDR_SIZE[dataName]
        wordLengthByte = (hex(wordLength)).replace('0x','').replace('0X','').zfill(2).encode('ascii')

        if wordLength == 1: # RSS
            readCmd = b'RSS0106' + readAddrByte
        else:               # RSB
            readCmd = b'RSB06' + readAddrByte + wordLengthByte
        return b'\x05' + STATION_NO + readCmd + b'\x04'
    return MakeReadCmd
# ===========================================================================================

def getPLCValue(ser:serial.Serial=None) -> str:
    getPLCRCmd = getPLCReadCmd()

    def getPLCRecv(dataName:str=None):

        if DEBUG:
            if dataName=='isRunning': return True
            recv = b'\x0601RSB010244413243003500000000\x03'
        else:
            ser.write(getPLCRCmd(dataName))
            recv = ser.readline() # ex) recv = b'\x0601RSS0102000A\x03'            
    # --------------------------
        def decodeResult() -> str:
            recvStr = recv.decode('ascii')
            resultStr = ''        
            if recv[1:3] != STATION_NO: 
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
    # --------------------------
    return getPLCRecv

def writeText(resList):
    FILE_HEADER = ['시간','프로그램번호','Bond명','Lot번호','RPM','설정시간','동작시간']
    resFileName = time.strftime("./output/%Y_%m_%d.txt", time.localtime())
    nowStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if not exists(resFileName):
        with open(resFileName, 'w') as f: 
            f.write('\t'.join(FILE_HEADER) + '\n')
    with open(resFileName, 'a') as f: 
        f.write('\t'.join([nowStr]+resList) + '\n')
    return

# ===========================================================================================
PLC_DATA = ['PrgNo','BondName','LotNo','RPM','TimeSet','TimeAct']
# -------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # how to find port ?
    # ser = serial.Serial('COM5',115200,timeout=1)
    ser=None
    getPLCResult = getPLCValue(ser)
    makedirs('./output', exist_ok=True)
    # --------------------------
    while True:
        isRunning = getPLCResult('isRunning')
        if isRunning == True:
            resList = []
            for dataName in PLC_DATA:
                res = getPLCResult(dataName)
                resList.append(res)
                print(dataName + ': ' + res)
            else:
                writeText(resList)
        time.sleep(.5)
    ser.close()
# ===========================================================================================
