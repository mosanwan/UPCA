from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os.path
import time
from time import strftime


class TreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        super(TreeModel, self).__init__(parent)


class MainWindow(QDialog):
    current_selected_plugin = ''
    current_selected_module = ''
    pluginPathDic = {}
    pluginModuleDic = {}
    pluginModulePathDic = {}
    pluginPCHDic = {}

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(600, 400)
        self.resize(500, 300)
        self.setWindowTitle("UPCA--虚幻引擎4插件代码自动创建工具(V 1.0)")
        self.check_author_info()
        self.code_analyse()
        # self.create_menu()
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.create_tree())
        main_layout.addWidget(self.create_right_panel())
        # main_layout.addStretch()
        self.setLayout(main_layout)

    def check_author_info(self):
        pass

    def get_copyright_info_temp(self):
        f = open("copyright.ini", 'r')
        copyright_str = f.read()
        copyright_str = copyright_str.replace("$classinfo$",
                                              self.classinfo.toPlainText())
        copyright_str = copyright_str.replace("$time$",
                                              time.strftime("%Y-%m-%d %X",
                                                            time.localtime()))
        return copyright_str

    def get_pch_file(self):
        return self.pluginPCHDic[self.current_selected_module]

    def create_slate_class(self):
        print("create slate")
        if self.headerNameEdit.text()[0] != 'S':
            QMessageBox.about(self, "", "Slate的类必须以 S 开头")
            return
        h_template_f = open("templates/slate.h.template", 'r')
        h_str = h_template_f.read()
        base_path = self.pluginModulePathDic[self.current_selected_module]
        h_path = base_path + "\\" + self.headerFileLocCombox.currentText() + "\\" \
                 + self.headerNameEdit.text()
        cpp_path = base_path + "\\" + self.cppFileLocCombox.currentText() + "\\" \
                   + self.cppNameEdit.text()

        h_str = h_str.replace("$classname$", self.classNameEdit.text())
        h_str = h_str.replace("$API$", self.get_header_api_marcro())
        h_str = h_str.replace("$authorinfo$", self.get_copyright_info_temp())

        h_write = open(h_path, 'w+', encoding='utf8')
        h_write.write(h_str)

        cpp_template_f = open("templates/slate.cpp.template", 'r')
        cpp_str = cpp_template_f.read()
        cpp_str = cpp_str.replace("$classname$", self.classNameEdit.text())
        cpp_str = cpp_str.replace("$pchfile$", self.get_pch_file())
        cpp_write = open(cpp_path, 'w+', encoding='utf8')
        cpp_write.write(cpp_str)

        QMessageBox.about(self, "", "创建成功")
        pass

    def get_header_api_marcro(self):
        if self.add_module_api.isChecked():
            return self.current_selected_module.upper() + "_API"
        else:
            return ""

    def create_class(self):
        if self.parentClassCombox.currentText() == "SCompoundWidget":
            self.create_slate_class()
        pass

    def create_tree(self):
        view = QTreeWidget()

        view.itemPressed.connect(self.tree_select)
        view.setHeaderLabel("选择你要操作的模块")
        for i in self.pluginPathDic:
            plugin_lab = QTreeWidgetItem(view)
            plugin_lab.setText(0, i)
            modules = self.pluginModuleDic[i]
            for j in modules:
                module_lab = QTreeWidgetItem(plugin_lab)
                module_lab.setText(0, j)
        view.setFixedWidth(200)
        return view

    def create_right_panel(self):
        group = QGroupBox('')
        layout = QVBoxLayout()
        self.classNameEdit = QLineEdit()
        self.classNameEdit.textChanged.connect(self.on_classNameChange)
        self.headerNameEdit = QLineEdit()
        self.headerNameEdit.setEnabled(False)
        self.cppNameEdit = QLineEdit()
        self.cppNameEdit.setEnabled(False)
        self.parentClassCombox = QComboBox()
        self.parentClassCombox.addItems(["None", "AActor", "UObject", "SCompoundWidget"])
        self.headerFileLocCombox = QComboBox()
        self.headerFileLocCombox.addItems(["Public", "Private", "Classes"])
        self.cppFileLocCombox = QComboBox()
        self.cppFileLocCombox.addItems(["Private", "Classes", "Public"])

        grid = QGridLayout()
        grid.addWidget(QLabel("名  称"), 0, 0)
        grid.addWidget(self.classNameEdit, 0, 1)
        grid.addWidget(QLabel("父类"), 0, 2)
        grid.addWidget(self.parentClassCombox, 0, 3)

        grid.addWidget(QLabel("头文件"), 1, 0)
        grid.addWidget(self.headerNameEdit, 1, 1)
        grid.addWidget(QLabel("位置"), 1, 2)
        grid.addWidget(self.headerFileLocCombox, 1, 3)

        grid.addWidget(QLabel("源文件"), 2, 0)
        grid.addWidget(self.cppNameEdit, 2, 1)
        grid.addWidget(QLabel("位置"), 2, 2)
        grid.addWidget(self.cppFileLocCombox, 2, 3)
        layout.addLayout(grid)

        self.add_module_api = QCheckBox("在类名前添加 XXX_API")
        # self.add_module_api.hide()
        layout.addWidget(self.add_module_api)

        self.generated_class_type = QComboBox()
        self.generated_class_type.addItems(["GENERATED_BODY", "GENERATED_UCLASS_BODY"])
        self.generate_box = QHBoxLayout()
        self.generate_box.addWidget(QLabel("选择类宏(仅对A、U 类型有效)"))
        self.generate_box.addWidget(self.generated_class_type)
        self.generate_box.addStretch()
        layout.addLayout(self.generate_box)

        self.classinfo = QTextEdit()
        self.classinfo.setText("类描述")
        layout.addWidget(self.classinfo)

        layout.addStretch()
        create_button = QPushButton("创建类")
        create_button.setFixedHeight(50)
        create_button.clicked.connect(self.create_class)
        layout.addWidget(create_button)
        group.setLayout(layout)
        return group

    def on_classNameChange(self):
        text = self.sender().text()
        print("class Name Change" + text)
        self.headerNameEdit.setText(text + ".h")
        self.cppNameEdit.setText(text + ".cpp")
        pass

    def tree_select(self):
        self.current_selected_module = self.sender().selectedItems()[0].text(0)
        try:
            print(self.pluginModulePathDic[self.current_selected_module])
            public_api_str = self.current_selected_module.upper()
            self.add_module_api.setText("在类名前添加 " + public_api_str + "_API")
            self.add_module_api.show()
        except Exception as e:
            print(e)
        pass

    def create_menu(self):
        self.menuBar().addMenu("&设置")
        self.menuBar().addMenu("&关于")
        pass

    def code_analyse(self):
        self.mudules = []
        current_path = os.getcwd()
        parent_path = os.path.dirname(current_path)
        plugin_path = parent_path + "\plugins"
        plugin_name = ""
        module_name = ""
        for parent, dirnames, filenames in os.walk(plugin_path):
            for filename in filenames:
                if filename.find(".uplugin") != -1:
                    path = parent + "\\" + filename
                    name = filename.split('.')[0]
                    plugin_name = name
                    self.pluginPathDic[name] = path
                    self.pluginModuleDic[plugin_name] = []

                if filename.find(".Build.cs") != -1:
                    path = parent + "\\" + filename
                    # print(path)
                    name = filename.split(".")[0]
                    module_name = name
                    self.pluginModulePathDic[name] = parent
                    self.pluginModuleDic[plugin_name].append(module_name)
                    pass
                if filename.find('PCH.h') != -1:
                    pch_name = filename
                    self.pluginPCHDic[module_name] = pch_name
                    print(pch_name)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    exit(app.exec())
