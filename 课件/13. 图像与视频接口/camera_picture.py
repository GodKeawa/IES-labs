#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cv2

cap = cv2.VideoCapture(0)  # 获取摄像头句柄,只连接一个摄像头时参数写0即可
i = 1  # 照片序号

while True:
    ret, frame = cap.read()  # 读一帧
    cv2.imshow("display", frame)  # 显示
    key = cv2.waitKey(1) & 0xFF  # 检测键盘,最长等待1ms (注意0表示永远而非0ms)
    if key == ord('p'):
        cv2.imwrite("image"+str(i)+".jpg", frame)  # 按p时保存图片
        i = i + 1
    if key == ord('q'):
        break  # 按q时退出

cap.release()  # 释放摄像头
cv2.destroyAllWindows()  # 关闭所有显示窗体
