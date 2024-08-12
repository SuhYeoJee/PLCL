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

    # lineEdit
    # pushButton

    def set_text_PROGRAM_TABLE(self, key, val)->None:
        i = int(''.join(filter(str.isdigit, key)))
        for j,item in enumerate(["STEPDIMENSION","CHARGEDIMENSION","FWDTIME","SELECTCAR","OSCCOUNT","BWDTIME","PRESSPOSITION","FINALPRESSURE","SELECTDIA"]):
            if not (item in key): continue
            self.PROGRAM_TABLE.setItem(i, j, QTableWidgetItem(val))


# ===========================================================================================
if __name__ == "__main__":
    app = QApplication([])
    window = View()
    window.show()
    app.exec_()

