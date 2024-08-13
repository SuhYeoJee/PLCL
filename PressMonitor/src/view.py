if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCL\PressMonitor")
# -------------------------------------------------------------------------------------------
from src.module.pyqt_imports import *
# ===========================================================================================

class View(QMainWindow, uic.loadUiType("./ui/untitled.ui")[0]) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.PROGRAM_TABLE.setHorizontalHeaderLabels(["STEP\nDIMENSION","CHARGE\nDIMENSION","FWD\nTIME","SELECT\nCAR","OSC\nCOUNT","BWD\nTIME","PRESS\nPOSITION","FINAL\nPRESSURE","SELECT\nDIA"])

    def set_text_PROGRAM_TABLE(self, key, val)->None:
        i = int(''.join(filter(str.isdigit, key)))-1
        for j,item in enumerate(["STEPDIMENSION","CHARGEDIMENSION","FWDTIME","SELECTCAR","OSCCOUNT","BWDTIME","PRESSPOSITION","FINALPRESSURE","SELECTDIA"]):
            if not (item in key): continue
            self.PROGRAM_TABLE.setItem(i, j, QTableWidgetItem(val))

    def set_text_PROGRAM_LIST_TABLE(self, key, val)->None:
        i = int(''.join(filter(str.isdigit, key)))-1
        j = (i//10)*2+1
        i = i%10
        self.PROGRAM_LIST_TABLE.setItem(i, j, QTableWidgetItem(val))

        for j,item in enumerate(["STEPDIMENSION","CHARGEDIMENSION","FWDTIME","SELECTCAR","OSCCOUNT","BWDTIME","PRESSPOSITION","FINALPRESSURE","SELECTDIA"]):
            if not (item in key): continue
            self.PROGRAM_LIST_TABLE.setItem(i, j, QTableWidgetItem(val))

    def set_text_PROGRAM_VIEW_TABLE(self, key, val)->None:
        i = int(''.join(filter(str.isdigit, key)))-1
        for j,item in enumerate(["STEPDIMENSION","CHARGEDIMENSION","FWDTIME","SELECTCAR","OSCCOUNT","BWDTIME","PRESSPOSITION","FINALPRESSURE","SELECTDIA"]):
            if not (item in key): continue
            self.PROGRAM_VIEW_TABLE.setItem(i, j, QTableWidgetItem(val))


# ===========================================================================================
if __name__ == "__main__":
    app = QApplication([])
    window = View()
    window.show()
    app.exec_()

