if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCL\PressMonitor")
# -------------------------------------------------------------------------------------------
from random import randint
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
        