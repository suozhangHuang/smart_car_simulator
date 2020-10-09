# -*- coding: utf-8 -*-
# @Time       : 2020/10/9 15:26
# @Author     : HuangJunli
# @FileName   : main.py
# @Description: PyQt5程序入口。在此新建主窗口。

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from main_win import *

app = QApplication(sys.argv)
ex = mainWin()
sys.exit(app.exec_())

