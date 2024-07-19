import sys

from PyQt5 import Qt
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView

from gui import *
from my_class import *

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap
import sys




class main_win(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = Ui_mainWindow()
        self.main_ui.setupUi(self)
        #self.setAttribute(Qt.WA_DeleteOnClose)
        self.main_ui.timepiece_lineEdit.setValidator(QIntValidator(100, 2000, self)) # 时间片100-2000

        self.main_ui.ready_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_ui.in_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_ui.out_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_ui.wait_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.timer = QTimer(self)
class connect_win:
    def __init__(self):
        self.window = main_win()
        self.bll = rr(self.window)

        self.connect()
        self.window.show()
    def connect(self):
        self.window.main_ui.OpenFile.triggered.connect(self.bll.InitQue)
        self.window.timer.timeout.connect(self.bll.RunOneTimeRange)
        self.window.main_ui.start_pushButton.clicked.connect(self.bll.StartTimer)
        self.window.main_ui.suspend_pushButton.clicked.connect(self.bll.EndTimer)

if __name__=='__main__':
    app = QApplication(sys.argv)
    win = connect_win()
    sys.exit(app.exec_())