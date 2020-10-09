# -*- coding: utf-8 -*-
# @Time       : 2020/10/9 15:24
# @Author     : HuangJunli
# @FileName   : main_win.py.py
# @Description: 程序入口，在此进行仿真设置。

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class mainWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        self._init_menubar()
        self._init_center_widget()

        self.setWindowTitle('Smart Car Simulator')
        self.resize(800, 600)
        self.show()

    def _init_menubar(self):
        # 获取菜单栏
        menubar = self.menuBar()

        # 配置
        file_menu = menubar.addMenu('&File')

        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    def _init_center_widget(self):
        label = QLabel('Helloworld')

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addStretch(1)

        central_widget = QWidget()
        central_widget.setLayout(vbox)
        self.setCentralWidget(central_widget)
