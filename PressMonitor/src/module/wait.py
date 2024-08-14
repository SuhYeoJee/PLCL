if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCL\PressMonitor")
    sys.path.append(r"C:\Users\gun07\Desktop\PLCL\PressMonitor")

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
    
    def get_dataset(self):
        try:
            dataset_list = self.dataset["PLC_ADDR"]
            self.dataset.pop("PLC_ADDR")
            for i in dataset_list:
                self.dataset.update(self.addrs["PLC_ADDR"][i])
        except Exception as e:
            print(e)
            ...
        print(self.dataset)



# -------------------------------------------------------------------------------------------
class test_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["TEST"]
        self.key = "ALARM_SV1_ALARM"

    def _is_next(self,val)->bool:
        """
        state 전환 조건 정의
        """
        return True if val[-1] == '0' else False
# -------------------------------------------------------------------------------------------
class connect_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["CONNECT"]
        self.get_dataset()
        self.key = "SYSTEM_ON"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False
# -------------------------------------------------------------------------------------------
class start_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["START"]
        self.get_dataset()
        self.key = "SYSTEM_RUN"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False
# -------------------------------------------------------------------------------------------
class exit_wait(state_wait):
    def __init__(self):
        super().__init__()
        self.dataset = self.addrs["DATASET"]["EXIT"]                
        self.get_dataset()
        self.key = "SYSTEM_RUN"

    def _is_next(self,val)->bool:
        return True if val[-1] == '0' else False
# ===========================================================================================

if __name__ == "__main__":
    m = exit_wait()
    m.get_dataset()