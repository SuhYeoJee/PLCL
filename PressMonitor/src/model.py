if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCL\PressMonitor")
    sys.path.append(r"C:\Users\gun07\Desktop\PLCL\PressMonitor")
# -------------------------------------------------------------------------------------------
from src.module.plc import test_plc
from src.module.wait import test_wait, connect_wait, start_wait, exit_wait
# --------------------------
from configparser import ConfigParser
# ===========================================================================================
class Model():
    def __init__(self):
        self.config = self.get_config()
        self.plc = test_plc()
        self._init_state()

    def _init_state(self)->None:
        self.t_w = test_wait()
        self.c_w, self.s_w, self.e_w = connect_wait(), start_wait(), exit_wait()
        self.t_w.next_state = self.c_w
        self.c_w.next_state = self.s_w
        self.s_w.next_state = self.e_w
        self.e_w.next_state = self.s_w
        # --------------------------
        self.state = self.t_w

    # [PLC] -------------------------------------------------------------------------------------------
    def _get_update_data(self)->dict:
        return self.plc.get_plc_dataset(self.state.dataset)

    def _change_mode(self)->None:
        self.state = self.state.next_state

    def worker_tick(self)->dict:
        update_data = self._get_update_data() # plc 데이터 읽기
        print(update_data)
        is_next = self.state._is_next(update_data[self.state.key]) # 읽은 항목에서 state체크
        if is_next: # state 넘어가기
            self._change_mode()
        return update_data

    # [config] -------------------------------------------------------------------------------------------
    def get_config_item(self,item:str="text"):
        return self.config.get(item,"val")
    
    def get_config(self,section:str="DEFAULT",config_path:str="config.txt",enc:str="utf-8"):
        config = ConfigParser()
        config.read(config_path,enc)
        return config[section]

# ===========================================================================================
if __name__ == "__main__":
    m = Model()
    ## config test
    # print(m.get_config_item('t'))
    ## json test
    # print(m.state.addrs["PLC_ADDR"]["AUTOMATIC"]["PRGNO"])
    ## ADDR PASING
    # print(m.plc.get_plc_data('DW100'))
    # print(m.plc.get_plc_data('DW100#21'))
    ## worker tick test
    # for i in range(100):
    #     print(m.worker_tick())


