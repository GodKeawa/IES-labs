#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import time
import sys

# client program
print("######################### TCP client #########################")

# server的IP和端口:
HOST_IP = "127.0.0.1"  # 与server端程序相同
HOST_PORT = 8888  # 与server端程序相同

# 创建socket:
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

i = 0
while True:
    try:
        # 连接server:  socket.connect(address)
        print("connecting to server...")
        socket_tcp.connect((HOST_IP, HOST_PORT))
        break
    except Exception:
        print("fail, retry later...")
        i += 1
        # 失败5次, 放弃:
        if i == 5:
            print("fail!")
            sys.exit(1)
        # 否则, 1s后重试:
        time.sleep(1)
print("succeed!")

# 接收欢迎信息:
data_recv = socket_tcp.recv(512)
print("received:", data_recv.decode())

while True:
    try:
        data_send = input(
            "message to send: "
        )  # 注意python2中input和raw_input的区别, raw_input返回值为字符串
        # 向server发送字符:
        socket_tcp.send(data_send.encode())
        # 发送exit, 结束会话:
        if data_send == "exit":
            break
        # 否则, 从server接收回复:
        data_recv = socket_tcp.recv(512)
        print("received:", data_recv.decode())
    except Exception:
        print("error!")
        socket_tcp.close()
        sys.exit(1)

# 关闭socket:
socket_tcp.close()
