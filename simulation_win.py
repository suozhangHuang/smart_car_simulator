# -*- coding: utf-8 -*-
# @Time       : 2020/10/14 20:44
# @Author     : HuangJunli
# @FileName   : simulation_win.py.py
# @Description: 仿真窗口
import sys

import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from simulation_backend import *

class simulationWin(QWidget):
    def __init__(self, simulation_backend):
        super().__init__()

        # 设置仿真后端
        self.simulation_backend = simulation_backend
        self.car = self.simulation_backend.get_car()
        self.map = self.simulation_backend.get_map()

        # 初始化用户界面
        self._init_ui()

        # 初始化时钟
        self.timer = QBasicTimer()
        self.time = 0
        self.tick = 20

    def timer_start(self):
        self.timer.start(self.tick, self)

    def timer_stop(self):
        self.timer.stop()

    def _init_ui(self):
        pass

    def timerEvent(self, event):
        self.time += self.tick
        self.simulation_backend.update(self.tick/1000, self.time/1000)

        self.update()

    def paintEvent(self, event):
        qpainter = QPainter()
        qpainter.begin(self)
        qpainter.setRenderHint(QPainter.Antialiasing, True)

        self._draw_map(qpainter)
        self._draw_car(qpainter)

        qpainter.end()

    def _draw_map(self, qpainter):
        win_w = self.size().width()
        win_h = self.size().height()

        point_SW = self.car['pos'] - np.array([win_w, win_h])/2
        point_NE = self.car['pos'] + np.array([win_w, win_h])/2
        if point_NE[0] > self.map['width']:
            point_SW[0] -= (point_NE[0] - self.map['width'])
            point_NE[0] -= (point_NE[0] - self.map['width'])
        if point_NE[1] > self.map['height']:
            point_SW[1] -= (point_NE[1] - self.map['height'])
            point_NE[1] -= (point_NE[1] - self.map['height'])
        if point_SW[0] < 0:
            point_NE[0] += (-point_SW[0])
            point_SW[0] += (-point_SW[0])
        if point_SW[1] < 0:
            point_NE[1] += (-point_SW[1])
            point_SW[1] += (-point_SW[1])
        self.win_SW = point_SW

        # 绘制地图地板图案
        target = QRect(QPoint(0, 0), self.size())
        source = QRect(QPoint(point_SW[0], point_SW[1]), self.size())
        qpainter.drawImage(target, self.map['floor_color_qimg'], source)

    def _draw_car(self, qpainter):
        polygon = []
        for p in self.simulation_backend._get_rect(self.car['pos'], self.car['size'], self.car['angle']):
            polygon.append(QPointF(p[0]-self.win_SW[0], p[1]-self.win_SW[1]))

        qpainter.setPen(Qt.transparent)
        qpainter.setBrush(Qt.gray)
        qpainter.drawPolygon(QPolygonF(polygon))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = simulationWin(simulationBackend())
    ex.timer_start()
    ex.show()
    sys.exit(app.exec_())


