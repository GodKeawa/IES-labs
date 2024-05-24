#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# debug 切换器
DEBUGSWITCH = False
LINUX = False
VIDEO = True

import numpy as np
import cv2

# global variables
# camera,width,height # 相机实例及参数
# frame # 原图
# binary 二值化图
# (x,y) 方向指向坐标


# 设置摄像头及图像清晰度，这里直接用opencv的接口了
def Camera_init():
    global camera, width, height
    width, height = 800, 640
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def TrackBar_Init():
    # 1 创建窗口
    cv2.namedWindow("variables control")
    if VIDEO:
        cv2.namedWindow("Video")
    # 2 创建TrackBar到窗口上，默认参数设置一下
    cv2.createTrackbar("hmin", "variables control", 10, 255, call_back)
    cv2.createTrackbar("hmax", "variables control", 20, 255, call_back)
    cv2.createTrackbar("smin", "variables control", 100, 255, call_back)
    cv2.createTrackbar("smax", "variables control", 255, 255, call_back)
    cv2.createTrackbar("vmin", "variables control", 100, 255, call_back)
    cv2.createTrackbar("vmax", "variables control", 255, 255, call_back)
    #   创建滑动条     滑动条值名称 窗口名称   滑动条值 滑动条阈值 回调函数


# 回调函数
def call_back(*arg):
    pass


# 在HSV色彩空间下得到二值图
def Get_HSV(image):
    global DEBUGSWITCH
    # 1 获取TrackBar设置的值
    hmin = cv2.getTrackbarPos("hmin", "variables control")
    hmax = cv2.getTrackbarPos("hmax", "variables control")
    smin = cv2.getTrackbarPos("smin", "variables control")
    smax = cv2.getTrackbarPos("smax", "variables control")
    vmin = cv2.getTrackbarPos("vmin", "variables control")
    vmax = cv2.getTrackbarPos("vmax", "variables control")

    # 2 转换到 HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    if DEBUGSWITCH:
        cv2.imshow("hsv", hsv)
        cv2.waitKey()

    # 3 设置范围，使用inRange函数
    # if value in (min, max):white; otherwise:black
    binary = cv2.inRange(
        hsv, np.array([hmin, smin, vmin]), np.array([hmax, smax, vmax])
    )
    if DEBUGSWITCH:
        cv2.imshow("binary", binary)
        cv2.waitKey()

    return binary


# 可选图像处理，不处理也行
def Image_Processing():
    global frame, binary
    # Capture the frames
    if LINUX:
        ret, frame = camera.read()

    # to binary
    binary = Get_HSV(frame)

    # 可选操作
    if False:
        blur = cv2.GaussianBlur(binary, (5, 5), 0)
        if DEBUGSWITCH:
            cv2.imshow("blur", blur)
            cv2.waitKey()

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 35))
        Open = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)
        if DEBUGSWITCH:
            cv2.imshow("Open", Open)
            cv2.waitKey()

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        Erode = cv2.morphologyEx(Open, cv2.MORPH_ERODE, kernel)
        if DEBUGSWITCH:
            cv2.imshow("Erode", Erode)
            cv2.waitKey()

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
        Dilate = cv2.morphologyEx(Erode, cv2.MORPH_DILATE, kernel)
        if DEBUGSWITCH:
            cv2.imshow("Dilate", Dilate)
            cv2.waitKey()

        binary = binary  # Anyone best


# 找线
def Find_Line():
    global x, y, image, width, height
    # 1 找出所有轮廓
    # 参数可调
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE
    )

    # 2 找出最大轮廓 -> 我们的只有橙色是白的，所以大概率只有一个轮廓，主要考虑交叉路口
    if len(contours) > 0:
        # 最大轮廓
        c = max(contours, key=cv2.contourArea)
        # 提取特征
        M = cv2.moments(c)

        # 中心点坐标
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        # print(x, y)

        # 显示
        image = frame.copy()
        # 标出中心位置及运动趋向
        cv2.line(image, (x, 0), (x, height), (0, 0, 255), 1)
        cv2.line(image, (0, y), (width, y), (0, 0, 255), 1)
        cv2.line(image, (width // 2, height), (x, y), (0, 255, 0), 3)
        cv2.line(image, (width // 2, 0), (width // 2, height), (0, 255, 0), 3)
        # 画出轮廓
        cv2.drawContours(image, contours, -1, (128, 0, 128), 2)
        cv2.imshow("Video", image)
        cv2.waitKey()

    else:
        print("not found the line")
        (x, y) = (0, 0)


if __name__ == "__main__":
    imgpath = "images/test4.png"
    frame = cv2.imread(imgpath, cv2.IMREAD_COLOR)
    # 暂时设置width和height
    width, height = 800, 640
    TrackBar_Init()
    while True:
        key = cv2.waitKey() & 0xFF  # anykey except q to continue
        Image_Processing()  # 可选择额外的处理
        Find_Line()
        if key == ord("q"):
            break
    cv2.destroyAllWindows()

