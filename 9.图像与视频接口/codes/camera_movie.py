#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cv2
import time

cap = cv2.VideoCapture(0)  # 获取摄像头句柄,只连接一个摄像头时参数写0即可
out = cv2.VideoWriter("movie.avi", cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), 17, (640, 480))  # 打开/新建视频文件用于写入,帧率=17,帧尺寸=640x480

while True:
    t = time.time()
    ret, frame = cap.read()  # 读一帧
    cv2.imshow("frame", frame)  # 显示
    out.write(frame)  # 写入视频文件
    key = cv2.waitKey(1) & 0xFF  # 检测键盘,最长等待1ms
    if key == ord('q'):
        break  # 按q时结束
    print (time.time() - t)

cap.release()  # 释放摄像头
out.release()  # 关闭视频文件
cv2.destroyAllWindows()  # 关闭所有显示窗体

