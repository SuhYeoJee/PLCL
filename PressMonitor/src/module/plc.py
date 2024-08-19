if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCL\PressMonitor")
    sys.path.append(r"C:\Users\gun07\Desktop\PLCL\PressMonitor")
# -------------------------------------------------------------------------------------------
from random import randint
import serial
import serial.tools.list_ports
# ===========================================================================================

class test_plc():
    def __init__(self):
        ...

    def _get_plc_word(self,addr:str,size:int=1)->str:
        return addr + '_' + str(size)  + '_' + str(randint(0,1))
    
    def _get_plc_bit(self,addr:str,size:int=1)->str:
        return addr + '_b' + (str(randint(0,1)) * size)
    
    def get_plc_data(self,addr:str)->str:
        addr,_,option = addr.partition('#')
        size = int(''.join(filter(str.isdigit, option)) or 1)
        if 'B' in option:
            return self._get_plc_bit(addr,size)
        else:
            return self._get_plc_word(addr,size)
    
    def get_plc_dataset(self,dataset:dict)->dict:
        return {k:self.get_plc_data(v) for k,v in dataset.items()}
        

class LS_plc():
    def __init__(self):
        self.stationNo = b'01' #국번(gukbun)
        self.ser = None
        self.isConnected = False
    # -------------------------------------------------------------------------------------------
    def connect(self):
        try:
            if not self.ser.is_open: 
                raise
        except:
            ports = serial.tools.list_ports.comports()
            if len(ports) == 1:
                portName = ports[0].device
            elif len(ports) == 0:
                print("연결된 장치 없음")
            else:
                for portInfo in ports:
                    print(f" - Device Name: {portInfo.device}")
                    print(f"   Serial Number: {portInfo.serial_number}")
                    print(f"   Vendor ID: {portInfo.vid}")
                    print(f"   Product ID: {portInfo.pid}")
                    print(f"   Description: {portInfo.description}")
                    print("\n")
                else:
                    portName = input("Device Name 입력: ").strip()
            try:
                self.ser = serial.Serial(portName,115200,timeout=1)
                self.isConnected = True
            except:
                self.ser = None
                self.isConnected = False
        else:
            self.isConnected = True
        finally:
            return self.isConnected
    # --------------------------
    def disconnect(self):
        try:
            self.ser.close()
        except:...
        finally:
            self.ser = None
            self.isConnected = False
            return self.isConnected    

    # ===========================================================================================
    def _get_read_cmd(self,addr:str,size:int=1)->bytes:
        addr_byte = b'%' + addr.encode('ascii')
        size_byte = (hex(size)).replace('0x','').replace('0X','').zfill(2).encode('ascii')
        if size == 1: 
            readCmd = b'RSS0106' + addr_byte # RSS
        else: 
            readCmd = b'RSB06' + addr_byte + size_byte # RSB
        return b'\x05' + self.stationNo + readCmd + b'\x04'
    
    def _get_plc_recv(self,cmd:bytes)->str:
        self.ser.write(cmd)
        recv = self.ser.readline() # ex) recv = b'\x0601RSS0102000A\x03'
        return recv.decode('ascii')

    def _get_recv_str(recvStr):
        resultStr = ''
        if recvStr.startswith('\x06'): # ACK
            if recvStr[3:6] == 'RSS':
                resultStr = str(int(recvStr[10:-1],16))
            elif recvStr[3:6] == 'RSB':
                hexStr = recvStr[10:-1]
                resultStr = ''.join([chr(int(hexStr[i+2:i+4], 16))+chr(int(hexStr[i:i+2], 16)) for i in range(0, len(hexStr), 4)])
            else: ... # not read result
        else: ... # not ACK
        return resultStr.replace('\x00','').strip()
    # --------------------------
    def get_plc_data(self,addr:str)->str:
        addr,_,option = addr.partition('#')
        size = int(''.join(filter(str.isdigit, option)) or 1)
        cmd = self._get_read_cmd(addr,size)
        recv = self._get_plc_recv(cmd)
        data = self._get_recv_str(recv)
        return data

    def get_plc_dataset(self,dataset:dict)->dict:
        return {k:self.get_plc_data(v) for k,v in dataset.items()}
        

if __name__ == "__main__":
    a = LS_plc()
    cmd = a._get_read_cmd("DW5004",1) #AUTOMATIC_PRGNO
    print("read [DW5004] CMD")
    print(cmd) #b'\x0501RSS0106%DW5004\x04'
    print("------------------")

    a.connect()
    res = a.get_plc_data("DW5004")
    print(res)