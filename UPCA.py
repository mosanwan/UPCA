from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os.path
import time
from time import strftime
from os.path import expanduser
import Templates


class MainWindow(QWidget):
    current_selected_plugin = ''
    current_selected_module = ''
    pluginPathDic = {}
    pluginModuleDic = {}
    pluginModulePathDic = {}
    pluginPCHDic = {}

    def __init__(self):
        super(MainWindow, self).__init__()
        self.user_ini = expanduser("~") + "\\.upca.ini"
        self.setMinimumSize(600, 400)
        self.resize(500, 300)
        self.setWindowTitle("UPCA--虚幻引擎4插件代码自动创建工具(V 1.1)")
        self.code_analyse()
        self.check_author_info()
        # self.create_menu()
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.create_tree())
        main_layout.addWidget(self.create_right_panel())
        # main_layout.addStretch()
        self.setLayout(main_layout)

    def check_author_info(self):
        if os.path.exists(self.user_ini):
            pass
            print("找到用户配置文件 " + self.user_ini)
        else:
            dialog = QDialog()
            self.userinfoDialog = dialog
            dialog.setWindowTitle("输入信息")
            dialog.setFixedSize(500, 500)
            dialogLayout = QVBoxLayout()
            dialogLayout.addWidget(QLabel("请输入一些用户信息，此信息将会出现在头文件版权声明中"))
            dialogLayout.addWidget(QLabel("配置文件存放路径："))
            dialogLayout.addWidget(QLabel(self.user_ini))
            dialog.setLayout(dialogLayout)
            grid = QGridLayout()
            grid.addWidget(QLabel("作者名"), 0, 0)
            self.authorname = QLineEdit()
            grid.addWidget(self.authorname, 0, 1)
            grid.addWidget(QLabel("Email"), 1, 0)
            self.authoremail = QLineEdit()
            grid.addWidget(self.authoremail, 1, 1)
            grid.addWidget(QLabel("个性签名"), 2, 0)
            self.authorsign = QLineEdit()
            grid.addWidget(self.authorsign, 2, 1)
            dialogLayout.addLayout(grid)
            dialogLayout.addStretch()
            ok = QPushButton("确定")
            dialogLayout.addWidget(ok)
            ok.clicked.connect(self.update_user_info)
            dialog.exec_()
            print("写入用户配置文件 " + self.user_ini)
        pass

    def update_user_info(self):
        author_name = self.authorname.text()
        author_email = self.authoremail.text()
        author_sign = self.authorsign.text()
        if author_name != "" and author_email != "":
            info = Templates.user_ini_temp
            info = info.replace("$auhtorname$", author_name)
            info = info.replace("$authoremail$", author_email)
            info = info.replace("$sign$", author_sign)
            f = open(self.user_ini, "w+", encoding='utf8')
            f.write(info)
            self.userinfoDialog.accept()
        else:
            QMessageBox.about(self.userinfoDialog, "", "请填写完整的信息")
        pass

    def get_copyright_info_temp(self):
        f = open(self.user_ini, 'r')
        copyright_str = f.read()
        copyright_str = copyright_str.replace("$classinfo$",
                                              self.classinfo.toPlainText())
        copyright_str = copyright_str.replace("$time$",
                                              time.strftime("%Y-%m-%d %X",
                                                            time.localtime()))
        return copyright_str

    def get_pch_file(self):
        return self.pluginPCHDic[self.current_selected_module]

    def get_h_file_path(self):
        base_path = self.pluginModulePathDic[self.current_selected_module]
        h_path = base_path + "\\" + self.headerFileLocCombox.currentText() + "\\" \
                 + self.headerNameEdit.text()
        return h_path

    def get_cpp_file_path(self):
        base_path = self.pluginModulePathDic[self.current_selected_module]
        cpp_path = base_path + "\\" + self.cppFileLocCombox.currentText() + "\\" \
                   + self.cppNameEdit.text()
        return cpp_path

    def create_slate_class(self):
        if self.headerNameEdit.text()[0] != 'S':
            QMessageBox.about(self, "", "Slate的类必须以 S 开头")
            return
        h_str = Templates.slate_h_template
        h_str = h_str.replace("$classname$", self.classNameEdit.text())
        h_str = h_str.replace("$API$", self.get_header_api_marcro())
        h_str = h_str.replace("$authorinfo$", self.get_copyright_info_temp())
        h_write = open(self.get_h_file_path(), 'w+', encoding='utf8')
        h_write.write(h_str)
        cpp_str = Templates.slate_cpp_template
        cpp_str = cpp_str.replace("$classname$", self.classNameEdit.text())
        cpp_str = cpp_str.replace("$pchfile$", self.get_pch_file())
        cpp_write = open(self.get_cpp_file_path(), 'w+', encoding='utf8')
        cpp_write.write(cpp_str)
        QMessageBox.about(self, "", "创建成功")

    def get_header_api_marcro(self):
        if self.add_module_api.isChecked():
            return self.current_selected_module.upper() + "_API"
        else:
            h_str = Templates.none_h_class
            h_str.replace()
            return ""

    def create_none_class(self):
        h_str = Templates.none_h_class
        h_str = h_str.replace("$classname$", self.classNameEdit.text())
        h_str = h_str.replace("$API$", self.get_header_api_marcro())
        h_str = h_str.replace("$authorinfo$", self.get_copyright_info_temp())
        h_write = open(self.get_h_file_path(), 'w+', encoding='utf8')
        h_write.write(h_str)
        cpp_str = Templates.none_cpp_class_temp
        cpp_str = cpp_str.replace("$classname$", self.classNameEdit.text())
        cpp_str = cpp_str.replace("$pchfile$", self.get_pch_file())
        cpp_write = open(self.get_cpp_file_path(), 'w+', encoding='utf8')
        cpp_write.write(cpp_str)
        QMessageBox.about(self, "", "创建成功")
        pass

    def create_actor_class(self):
        h_str = Templates.actor_h_class
        h_str = h_str.replace("$classname$", self.classNameEdit.text())
        h_str = h_str.replace("$API$", self.get_header_api_marcro())
        h_str = h_str.replace("$authorinfo$", self.get_copyright_info_temp())
        generate_type = self.generated_class_type.currentText()
        h_str = h_str.replace("$genera$", generate_type)
        h_write = open(self.get_h_file_path(), 'w+', encoding='utf8')
        h_write.write(h_str)
        cpp_str = ''
        if generate_type == "GENERATED_BODY":
            cpp_str = Templates.actor_cpp_class_none_construct
        else:
            cpp_str = Templates.actor_cpp_class
        cpp_str = cpp_str.replace("$classname$", self.classNameEdit.text())
        cpp_str = cpp_str.replace("$pchfile$", self.get_pch_file())
        cpp_write = open(self.get_cpp_file_path(), 'w+', encoding='utf8')
        cpp_write.write(cpp_str)
        QMessageBox.about(self, "", "创建成功")
        pass

    def create_object_class(self):
        h_str = Templates.object_h_class
        h_str = h_str.replace("$classname$", self.classNameEdit.text())
        h_str = h_str.replace("$API$", self.get_header_api_marcro())
        h_str = h_str.replace("$authorinfo$", self.get_copyright_info_temp())
        generate_type = self.generated_class_type.currentText()
        h_str = h_str.replace("$genera$", generate_type)
        h_write = open(self.get_h_file_path(), 'w+', encoding='utf8')
        h_write.write(h_str)
        cpp_str = ''
        if generate_type == "GENERATED_BODY":
            cpp_str = Templates.object_cpp_class_none_construct
        else:
            cpp_str = Templates.object_cpp_class
        cpp_str = cpp_str.replace("$classname$", self.classNameEdit.text())
        cpp_str = cpp_str.replace("$pchfile$", self.get_pch_file())
        cpp_write = open(self.get_cpp_file_path(), 'w+', encoding='utf8')
        cpp_write.write(cpp_str)
        QMessageBox.about(self, "", "创建成功")
        pass

    def create_class(self):
        if self.parentClassCombox.currentText() == "SCompoundWidget":
            self.create_slate_class()
        if self.parentClassCombox.currentText() == "None":
            self.create_none_class()
        if self.parentClassCombox.currentText() == "AActor":
            self.create_actor_class()
        if self.parentClassCombox.currentText() == "UObject":
            self.create_object_class()
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
        self.headerNameEdit.setText(text + ".h")
        self.cppNameEdit.setText(text + ".cpp")
        pass

    def tree_select(self):
        self.current_selected_module = self.sender().selectedItems()[0].text(0)
        try:
            public_api_str = self.current_selected_module.upper()
            self.add_module_api.setText("在类名前添加 " + public_api_str + "_API")
            self.add_module_api.show()
        except Exception as e:
            pass
        pass

    def create_menu(self):
        self.menuBar().addMenu("&设置")
        self.menuBar().addMenu("&关于")
        pass

    def code_analyse(self):
        self.mudules = []
        plugin_path = os.getcwd() + "\\Plugins"
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
                    name = filename.split(".")[0]
                    module_name = name
                    self.pluginModulePathDic[name] = parent
                    self.pluginModuleDic[plugin_name].append(module_name)
                if filename.find('PCH.h') != -1:
                    pch_name = filename
                    self.pluginPCHDic[module_name] = pch_name


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
