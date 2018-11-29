# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

INPUT_LIMIT = 10


# 重写控件焦点事件
class MyQLineEdit(QLineEdit):
    def __init__(self, *__args, main_window):
        self.ui_main_window = main_window
        super().__init__(*__args)

    def focusInEvent(self, e):
        self.ui_main_window.status_handler()
        QLineEdit.focusInEvent(self, e)  # 还原功能

    def focusOutEvent(self, e):
        self.ui_main_window.status_handler()
        QLineEdit.focusOutEvent(self, e)  # 还原功能


class Ui_MainWindow(object):

    def __init__(self):
        # 控件基准坐标
        self.base_pos = {'x': 180, 'y': 50}
        # 目标路径
        self.url = None

    # 状态处理函数
    def status_handler(self):
        if self.url is None or len(self.url) == 0:
            self.statusbar_conf('blue', '请选择目标文件夹')
            # 禁用按钮
            self.pushButton.setEnabled(0)
        else:
            self.statusbar_conf('green', '即将处理目录：%s' % self.url)
            # 启用按钮
            self.pushButton.setEnabled(1)

    def setupUi(self, MainWindow):

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.statusbar = QStatusBar(MainWindow)
        self.oldExtension = MyQLineEdit(self.centralwidget, main_window=self)
        self.newExtension = MyQLineEdit(self.centralwidget, main_window=self)
        self.targetDirBtn = QPushButton(self.centralwidget)

        # 导入qss
        with open('css.qss') as file:
            style_sheet = ''.join(file.readlines()).strip('\n')
        MainWindow.setStyleSheet(style_sheet)

        # 调用模块
        self.main_handler()
        self.target_dir()
        self.old_data_handler()
        self.new_data_handler()
        self.label_btn_handler()
        self.statusbar_handler()
        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def main_handler(self):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(720, 460)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        # MainWindow.setSizePolicy(sizePolicy)
        # 主窗口背景色
        # 实例化主窗口的QMenuBar对象
        bar = QMenuBar()
        # 向菜单栏中添加新的QMenu对象，父菜单
        fun = bar.addMenu('功能')
        about = bar.addMenu('其他')
        # 向QMenu小控件中添加按钮，子菜单
        fun.addAction('打开目录')
        about.addAction('帮助')
        about.addAction('关于')
        MainWindow.setMenuBar(bar)

    def target_dir(self):
        self.targetDirBtn.setGeometry(QRect(self.base_pos['x'] + 50, self.base_pos['y'] + 160, 290, 50))
        self.targetDirBtn.setText('选择目录')
        self.targetDirBtn.clicked.connect(self.choose_dir)

    def old_data_handler(self):
        old_label = QLabel(self.centralwidget)
        old_label.setGeometry(QRect(self.base_pos['x'] - 20, self.base_pos['y'] + 46, 60, 24))
        old_label.setFont(QFont('Arial', pointSize=10))
        old_label.setText('原后缀:')

        self.oldExtension.setGeometry(QRect(self.base_pos['x'] + 50, self.base_pos['y'] + 40, 291, 40))
        self.oldExtension.setAlignment(Qt.AlignCenter)
        self.oldExtension.setObjectName("oldExtension")  # 原后缀
        self.oldExtension.setText('*')
        self.oldExtension.textChanged.connect(self.text_num_limit)
        # self.oldExtension.setFocusPolicy(QtCore.Qt.NoFocus)

    def new_data_handler(self):
        new_label = QLabel(self.centralwidget)
        new_label.setGeometry(QRect(self.base_pos['x'] - 20, self.base_pos['y'] + 106, 60, 24))
        new_label.setFont(QFont('Arial', pointSize=10))
        new_label.setText('新后缀:')

        self.newExtension.setGeometry(QRect(self.base_pos['x'] + 50, self.base_pos['y'] + 100, 291, 40))
        self.newExtension.setAlignment(Qt.AlignCenter)
        self.newExtension.setObjectName("newExtension")  # 新后缀
        self.newExtension.setFocus()
        self.newExtension.textChanged.connect(self.text_num_limit)

    def label_btn_handler(self):
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(self.base_pos['x'] + 50, self.base_pos['y'] + 230, 290, 50))
        # 默认禁止点击
        self.pushButton.setEnabled(0)
        self.pushButton.setObjectName("confirmBtn")
        # 核心函数
        self.pushButton.clicked.connect(self.startHandler)

    def statusbar_handler(self):
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar_conf('blue', '请选择目标文件夹')

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "批量修改后缀 v0.1"))
        self.pushButton.setText(_translate("MainWindow", "修改"))

    # 长度校验
    def text_num_limit(self):
        if self.oldExtension.hasFocus():
            obj = self.oldExtension
        else:
            obj = self.newExtension
        if len(obj.text()) > INPUT_LIMIT:
            # 截取前十个字符
            obj.setText(obj.text()[0:INPUT_LIMIT])
            self.statusbar_conf('red', '后缀过长，请检查')
        else:
            self.status_handler()

    # 状态栏定义
    def statusbar_conf(self, color, msg):
        self.statusbar.setStyleSheet(
            "QStatusBar {color:%s;}" % color)
        self.statusbar.showMessage(msg)

    # 选择目录
    def choose_dir(self):
        try:
            dir_ready = QFileDialog.getExistingDirectory(None, caption=str('选择'), directory='./')
            # print(dir_ready)
            # 成功
            if len(dir_ready) is not 0:
                self.url = dir_ready
            self.status_handler()
            self.newExtension.setFocus()
        except Exception as e:
            self.statusbar_conf('red', '错误！  %s' % e)

    # 开始处理
    def startHandler(self):
        # 进入目录
        os.chdir(self.url)
        # 获取数据
        old = self.oldExtension.text()
        new = self.newExtension.text()
        # 校验与提示
        if len(new) == 0 or len(old) == 0:
            error = QMessageBox.warning(None, "错误", "请填写完整信息")
            return
        if old == '*':
            # 弹窗警告
            reply = QMessageBox.question(None, "警告", "将把该文件夹下所有文件后缀修改为" + "\"" + new + "\"",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                return

        # 遍历
        for i in os.listdir(os.getcwd()):
            if os.path.isfile(i):
                # 对比后缀名
                index = i.rfind('.')
                if old == '*':
                    os.rename(os.getcwd() + '/' + i, os.getcwd() + '/' + i[0:index] + '.' + str(new))
                else:
                    if i[index + 1:] == old:
                        os.rename(os.getcwd() + '/' + i, os.getcwd() + '/' + i[0:index] + '.' + str(new))

        self.statusbar_conf('green', '完成！')
        QMessageBox.information(None, "结果", "处理完成")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
