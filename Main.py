from PyQt5.QtWidgets import *
import sys
import os.path


class MainWindow(QDialog):
    current_selected_plugin = ''
    current_selected_module = ''
    pluginPathDic = {}
    pluginModuleDic ={}

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(1200, 780)
        self.resize(800,600)
        self.setWindowTitle("UPCA--虚幻引擎4插件代码自动创建工具")
        self.code_analyse()
        #self.create_menu()

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.create_plugin_groupBox())
        main_layout.addWidget(self.create_mudule_groupBox())
        main_layout.addStretch()
        self.setLayout(main_layout)

    def create_mudule_groupBox(self):
        verticalGroupBox = QGroupBox("模块列表")
        self.module_layout = QVBoxLayout()
        for i in range(5):
            button = QPushButton("Button")
            self.module_layout.addWidget(button)
        self.module_layout.addStretch()
        verticalGroupBox.setLayout(self.module_layout)
        return verticalGroupBox

    def create_plugin_groupBox(self):
        verticalGroupBox = QGroupBox("插件列表")
        layout = QVBoxLayout()
        for i in self.pluginPathDic:
            button = QPushButton(i)
            button.clicked.connect(self.on_plugin_select)

            layout.addWidget(button)
        layout.addStretch()
        verticalGroupBox.setLayout(layout)
        return verticalGroupBox

    def on_plugin_select(self):
        self.current_selected_plugin = self.sender().text()
        self.show_modules()

    def show_modules(self):
        for i in range(self.module_layout.count()):
            pass
        for i in self.pluginModuleDic[self.current_selected_plugin]:
            button = QPushButton(i)
            self.module_layout.addWidget(button)
        self.module_layout.addStretch()

    def create_menu(self):
        self.menuBar().addMenu("&设置")
        self.menuBar().addMenu("&关于")
        pass

    def code_analyse(self):
        self.mudules = []
        current_path = os.getcwd()
        parent_path = os.path.dirname(current_path)
        plugin_path = parent_path+"\plugins"

        plugin_name = ""
        module_name = ""
        pch_name = ""

        for parent,dirnames,filenames in os.walk(plugin_path):
            for filename in filenames:
                if filename.find(".uplugin") != -1:
                    path = parent+"\\"+filename
                    name = filename.split('.')[0]
                    plugin_name = name
                    self.pluginPathDic[name] = path
                    self.pluginModuleDic[plugin_name] = []

                if filename.find(".Build.cs") != -1:
                    path = parent+"\\"+filename
                    print(path)
                    name = filename.split(".")[0]
                    module_name = name
                    self.pluginModuleDic[plugin_name].append(module_name)
                    pass


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    exit(app.exec())



