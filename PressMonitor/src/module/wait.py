if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCL\PressMonitor")
# -------------------------------------------------------------------------------------------
import json
# ===========================================================================================

class state_wait():
    def __init__(self):
        self.addrs = self.get_plc_addrs()
        self.dataset = None
        self.next_state = None
        
    def _is_next(self,val)->bool:...
    # [json] -------------------------------------------------------------------------------------------
    def get_plc_addrs(self):
        with open("./src/spec/PLC_ADDR.json", 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data 

# -------------------------------------------------------------------------------------------
class test_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["TEST"]
        self.key = "ALARM_SV1_ALARM"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False
# -------------------------------------------------------------------------------------------
class connect_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["CONNECT"]
        self.key = "SYSTEM_ON"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False
# -------------------------------------------------------------------------------------------
class start_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["START"]
        self.key = "SYSTEM_RUN"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False
# -------------------------------------------------------------------------------------------
class exit_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["EXIT"]                
        self.key = "SYSTEM_ON"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False
# ===========================================================================================
