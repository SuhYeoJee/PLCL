import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 윈도우 설정
        self.setWindowTitle("Table Update Example")
        self.setGeometry(100, 100, 600, 400)

        # 데이터 변수
        self.program_prg1_fwdtime = "DW2103"

        # QTableWidget 생성
        self.tableWidget = QTableWidget(2, 2, self)
        self.tableWidget.setItem(0, 0, QTableWidgetItem("PROGRAM_PRG1_FWDTIME"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem(self.program_prg1_fwdtime))

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 타이머를 사용하여 주기적으로 데이터 갱신 (예제)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # 1초마다 update_data 호출

    def update_data(self):
        """데이터를 주기적으로 갱신 (예제)"""
        # 실제 애플리케이션에서는 데이터 변동이 있을 때 셀 값을 갱신
        new_value = "DW" + str(int(self.program_prg1_fwdtime[2:]) + 1)
        self.program_prg1_fwdtime = new_value
        self.tableWidget.item(0, 1).setText(new_value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
