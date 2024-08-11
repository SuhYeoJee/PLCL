if __debug__:
    import sys
    sys.path.append(r"D:\Github\PressMonitor")
# -------------------------------------------------------------------------------------------
from configparser import ConfigParser
# ===========================================================================================
class Model():
    def __init__(self):
        self.config = self.get_config()
        ...
    def get_val(self):
        return self.config.get("text","val")
    
    def get_config(self,section:str="DEFAULT",config_path:str="config.txt",enc:str="utf-8"):
        config = ConfigParser()
        config.read(config_path,enc)
        return config[section]
# ===========================================================================================
if __name__ == "__main__":
    m = Model()
    print(m.get_val())
