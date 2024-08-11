if __debug__:
    import sys
    sys.path.append(r"D:\Github\PLCL\PressMonitor")
# -------------------------------------------------------------------------------------------
from src.module.pyqt_imports import *
# ===========================================================================================

class View(QMainWindow, uic.loadUiType("./ui/MainWindow.ui")[0]) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

    # lineEdit
    # pushButton



# ===========================================================================================
if __name__ == "__main__":
    app = QApplication([])
    window = View()
    window.show()
    app.exec_()

