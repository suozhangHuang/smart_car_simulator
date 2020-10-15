# -*- coding: utf-8 -*-
# @Time       : 2020/10/14 20:56
# @Author     : HuangJunli
# @FileName   : simulation_backend.py.py
# @Description: 仿真计算部分，显示窗口从后端读取仿真数据
import cv2
import numpy as np
from PyQt5.QtGui import QImage

from random_map_generator.random_map import generate_random_map

class simulationBackend:
    def __init__(self):
        self.car = None
        self.map = None

        self._init_car()
        self._init_map()

    # 返回记录car数据的字典
    def get_car(self):
        return self.car

    # 返回记录map数据的字典
    def get_map(self):
        return self.map

    # 进行步长为tick的仿真
    def update(self, tick, time):
        # 检查是否与地图边界发生碰撞
        if self.map['border_barrier']:
            for p in self._get_rect(self.car['pos'], self.car['size'], self.car['angle']):
                if not self._in_map_border(p):
                    self.car['velocity'] = np.zeros(2)
                    self.car['angular_velocity'] = 0

        self.car['pos'] += self.car['velocity'] * tick
        self.car['angle'] += self.car['angular_velocity'] * tick

    def _init_car(self):
        self.car = {
            'size': np.array([100, 125]).astype('float64'),
            'pos': np.array([200, 150]).astype('float64'),
            'velocity': np.array([100, 150]).astype('float64'),
            'angle': 0.0,
            'angular_velocity': 0.2
        }

    def _init_map(self):
        img = generate_random_map(1000, 800, (800, 600), savepath='map.png')

        floor_color = img.transpose()
        height, width, channel = img.shape
        bytesPerline = 3 * width
        floor_color_qimg = QImage(img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()

        self.map = {
            'width': 1000,
            'height': 800,
            'border_barrier': True,
            'border_size': np.array([800, 600]),
            'inner_barrier': [],
            'floor_color': floor_color,
            'floor_color_qimg': floor_color_qimg
        }

    def _get_rect(self, center, size, angle):
        w = size[0]/2
        h = size[1]/2
        p1 = (h*np.cos(angle) - w*np.sin(angle) + center[0],
              w*np.cos(angle) + h*np.sin(angle) + center[1])
        p3 = (-h*np.cos(angle) + w*np.sin(angle) + center[0],
              -w*np.cos(angle) - h*np.sin(angle) + center[1])
        p2 = (-h*np.cos(angle) - w*np.sin(angle) + center[0],
              w*np.cos(angle) - h*np.sin(angle) + center[1])
        p4 = (h*np.cos(angle) + w*np.sin(angle) + center[0],
              -w*np.cos(angle) + h*np.sin(angle) + center[1])

        return p1, p2, p3, p4

    def _in_map_border(self, pos):
        border_dx = (self.map['width'] - self.map['border_size'][0])/2
        border_dy = (self.map['height'] - self.map['border_size'][1])/2
        if pos[0] > self.map['width']-border_dx or pos[0] < border_dx:
            return False
        if pos[1] > self.map['height']-border_dy or pos[1] < border_dy:
            return False
        return True