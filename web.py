import sys
import os.path
from PyQt5.QtWidgets import (QApplication,QWidget,QVBoxLayout)
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QUrl

class MainWin(QWebEngineView):
    def __init__(self):
        super(MainWin,self).__init__()
        self.load(QUrl(os.getcwd()+ "/html/app.html"))
        self.resize(800, 600)
        self.setMinimumSize(800, 600)
        self.setWindowTitle("UPCA--虚幻引擎4插件代码自动创建工具")

    def fun(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())