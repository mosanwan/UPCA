import sys
from PyQt5.QtWidgets import *


class BoxLayout(QWidget):
    def __init__(self):
        super(BoxLayout, self).__init__()
        self.ok_button = QPushButton("确定")
        self.cancel_button = QPushButton("取消")
        self.ok_button.clicked.connect(self.test_fun, 1)
        self.h_box = QHBoxLayout()
        self.h_box.addStretch(1)
        self.h_box.addWidget(self.ok_button)
        self.h_box.addWidget(self.cancel_button)

        self.v_box = QVBoxLayout()
        self.v_box.addStretch()
        self.v_box.addLayout(self.h_box)

        self.setLayout(self.v_box)

    def test_fun(self, event):
        print("Clicked")
        print(event)

app = QApplication(sys.argv)
layout = BoxLayout()
layout.show()
sys.exit(app.exec_())