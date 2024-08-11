if __debug__:
    import sys
    sys.path.append(r"D:\Github\PressMonitor")
# -------------------------------------------------------------------------------------------
from src.module.pyqt_imports import *
from src.module.window_builder import WindowBuilder
# ===========================================================================================
class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.wb = WindowBuilder()
        self.widgets = {}
        self.layouts = {}
        self.dialogs = {}        
        # --------------------------
        screen = QDesktopWidget().screenGeometry() # 화면 크기 조정
        self.resize(int(screen.width() * 0.5), int(screen.height() * 0.4))
        self.setWindowTitle("window_title")
        # --------------------------
        self.layouts['main'] = self.get_lay1()
        # --------------------------
        self.widgets['main'] = QWidget()
        self.widgets['main'].setLayout(self.layouts['main'])
        self.setCentralWidget(self.widgets['main'])
    # -------------------------------------------------------------------------------------------
    def get_lay1(self,val:str=''):
        lay1 = QVBoxLayout()
        self.widgets['main_text'] = self.wb.get_label(f"new project: {val}")
        lay1.addWidget(self.widgets['main_text'])
        return lay1
    
    def change_main_text(self,val:str=''):
        self.widgets['main_text'].setText(val)


# ===========================================================================================
if __name__ == "__main__":
    app = QApplication([])
    window = View()
    window.show()
    app.exec_()
