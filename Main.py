from PyQt5.QtWidgets import *
import sys
import os.path


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle("UPCA--虚幻引擎4插件代码自动创建工具")
        self.code_analyse()
        #self.create_menu()
        self.create_upluginGroupBox()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.create_upluginGroupBox())
        main_layout.addWidget(QLabel("Hello World"))
        self.setLayout(main_layout)

    def create_upluginGroupBox(self):
        upluginGroupBox = QGroupBox("Plugins")
        layout = QVBoxLayout()
        for i in range(4):
            layout.addWidget(QPushButton("B"))
            print("B")
        upluginGroupBox.setLayout(layout)
        return upluginGroupBox

    def create_menu(self):
        self.menuBar().addMenu("&设置")
        self.menuBar().addMenu("&关于")
        pass

    def code_analyse(self):
        current_path = os.getcwd()
        parent_path = os.path.dirname(current_path)
        plugin_path = parent_path+"\plugins"
        print(plugin_path)
        for parent,dirnames,filenames in os.walk(parent_path):
            for filename in filenames:
                if filename.find(".uplugin") != -1:
                    print("Plugin "+parent+"\\"+filename)
                if filename.find(".Build.cs") != -1:
                    #print("Mudule "+parent+"\\"+filename)
                    pass


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    exit(app.exec())



