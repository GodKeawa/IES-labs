#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import math

# 读取图片
img = cv2.imread("atest.png", cv2.IMREAD_COLOR)
imgcanny = cv2.Canny(img,100,200)
cv2.imwrite("acanny.jpeg",imgcanny)

# 转为灰度图像
#imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imggray = img
#cv2.imwrite("agray.jpeg", imggray)

# 高斯去噪，（3,3）表示高斯核大小
imggausse = cv2.GaussianBlur(imggray, (3, 3), 0)

cv2.imwrite("agausse.jpeg", imggausse)

# 二值化，80为阈值
ret, imgbinary = cv2.threshold(imggausse, 80, 255, cv2.THRESH_BINARY_INV)

imggray = cv2.cvtColor(imgbinary, cv2.COLOR_BGR2GRAY)
cv2.imwrite("agray.jpeg", imggray)
ret, imgbinary2 = cv2.threshold(imgbinary, 80, 255, cv2.THRESH_BINARY_INV)
cv2.imwrite("abinary.jpeg", imgbinary2)

# 边缘提取，50,150两个阈值比值应在1：2与1：3之间
# edges=cv2.Canny(imggray, 100, 200, apertureSize=3)

# 统计概率霍夫线变换
# threshold 检测一条直线所需的最少极坐标曲线交点数
threshold = 100
# minLineLength 组成一条直线的最小长度
minLineLength = 100
# maxLineGap 两条直线为同一条直线的最大间隙
maxLineGap = 100
lines = cv2.HoughLinesP(
    imgbinary, 1, math.pi / 180, threshold, minLineLength, maxLineGap
)

# 在原图上绘制直线
"""
for l in lines:
	for x1,y1,x2,y2 in l:
		cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
"""
for x1, y1, x2, y2 in lines[0]:
    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

# 显示图片
# 注：在图片窗口弹出后，键入任意键关闭窗口并结束程序
cv2.imshow("img", img)
cv2.waitKey()
cv2.destroyAllWindows()
