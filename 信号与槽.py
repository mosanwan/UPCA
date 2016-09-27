import sys
from PyQt5 import QtWidgets,QtCore


class EmitSigal(QtWidgets.QWidget):
    closeEmitApp = QtCore.pyqtSignal()

    def __init__(self):
        super(EmitSigal,self).__init__()
        self.setWindowTitle("信号与槽")
        self.resize(600, 800)
        self.closeEmitApp.connect(self.close)

    def mousePressEvent(self, QMouseEvent):
        self.closeEmitApp.emit()

app = QtWidgets.QApplication(sys.argv)
em = EmitSigal()
em.show()
sys.exit(app.exec_())