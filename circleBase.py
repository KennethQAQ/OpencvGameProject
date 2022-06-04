import random
from cv2 import circle

import pygame
import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector


class Circle:  # 暂时没用上的内部圆圈
    def __init__(self, posX, posY, surface, r=30, color=(0, 255, 0)):
        self.r = r
        self.color = color
        self.posX = posX
        self.posY = posY
        self.surface = surface

    def draw_circle(self):
        pygame.draw.circle(self.surface, self.color, [self.posX, self.posY], self.r)


class Ring:  # 暂时没用上的外环组件
    def __init__(self, posX, posY, surface, r=90, color=(0, 255, 0)):
        self.r = r
        self.color = color
        self.posX = posX
        self.posY = posY
        self.surface = surface

    def draw_ring(self):
        pygame.draw.circle(self.surface, self.color, [self.posX, self.posY], self.r, 2)


class Item:  # 主要组件-圆环
    def __init__(self, surface, r=30, R=120, color=(0, 255, 0)):
        self.circleR = r  # 内圆圈大小参数
        self.ringR = R  # 外圆环大小参数
        self.color = color  # 圆环颜色
        self.posX = 100  # 圆心X轴坐标参数
        self.posY = 200  # 圆心Y轴坐标参数
        self.surface = surface  # 图像对象
        self.score = 0  # 得分
        self.circle = Circle(self.posX, self.posY, self.surface)  # 内圆
        self.ring = Ring(self.posX, self.posY, self.surface)  # 外圈
        self.font = pygame.font.SysFont('宋体', 30, True)  # 得分显示的文字
        self.circlenumb = 0  # 测试参数得分测试时使用，忽略
        self.touchpointX = 0  # 手点击位置的X轴坐标
        self.touchpointY = 0  # 手点击位置的Y轴坐标

    def randomItemLocation(self):  # 随机生成坐标
        self.posX = random.randint(100, 1000)
        self.posY = random.randint(200, 600)

    def draw_item(self):  # 绘制组件
        pygame.draw.circle(self.surface, self.color, [self.posX, self.posY], self.circleR)  # 绘制内圆
        pygame.draw.circle(self.surface, self.color, [self.posX, self.posY], self.ringR, 2)  # 绘制外圈

    def showscore(self):  # 显示得分
        self.surface.blit(self.font.render(f'Your Score:%d' % self.score, True, [255, 0, 0]), [550, 100])

    def Ring2Circle(self):  # 关键游戏进程-圆环收拢过程  当圆环大小收拢和内圈大小一样时刷新下一个圆环
        if self.ringR == 30:
            self.randomItemLocation()
            self.circlenumb += 1
            self.ringR = 120
        else:
            self.ringR -= 3

    def getscore(self):  # 关键游戏进程-游戏得分更新  暂定正好在收拢时移动到位置加2分，收拢之前移动到位置中加1分 判定方式为看是否手指坐标在内圆半径以内
        # self.score = self.circlenumb
        if self.posX - self.ringR < self.touchpointX < self.posX + self.ringR and self.posY - self.ringR < self.touchpointY < self.posY + self.ringR:
            self.score += 1
            self.ringR = 30
