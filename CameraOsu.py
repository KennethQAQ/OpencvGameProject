import cv2
import numpy as np
import pygame
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time

from circleBase import Item

#   游戏主程序

pygame.init()

# create window
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("my game")

# Camera

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.7)

# initialize fps clock 
fps = 10    #速度参数
clock = pygame.time.Clock()

# main
firstItem = Item(window)

start = True
while start:

    # get events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # apply logic

    # Opencv

    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    if hands:
        # landmarkList
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]  # 2维手部骨骼食指坐标列表
        firstItem.touchpointX = pointIndex[0]
        firstItem.touchpointY = pointIndex[1]

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, True, False)
    window.blit(frame, (0, 0))

    # block logic
    
    firstItem.draw_item()
    firstItem.Ring2Circle()
    firstItem.showscore()
    firstItem.getscore()

    #update display
    pygame.display.update()

    # set fps
    clock.tick(fps)

    #结束游戏
    key = cv2.waitKey(1)
    if key == ord('x'):
        start = False
