#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys

# server program
print("######################### TCP server #########################")

# server的IP和端口:
HOST_IP = "127.0.0.1"  # 改为你的server(树莓派/PC)的IP地址！
HOST_PORT = 8888  # 0-65536, 选择无特殊含义的即可

# 创建socket:  socket.socket([family[, type[, proto]]]) -> socket, family: IP+port选AF_INET, type: TCP选SOCK_STREAM
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定IP和端口:  socket.bind(address)
socket_tcp.bind((HOST_IP, HOST_PORT))
# 监听连接请求:  socket.listen(backlog), backlog: 连接队列最大长度
socket_tcp.listen(1)
print("listen @ IP address:", HOST_IP, "port:", HOST_PORT)

# 接受client的连接请求:  socket.accept() -> (conn, address), conn: 用来收发数据的socket对象
socket_conn, (client_ip, client_port) = socket_tcp.accept()
print("connected by: IP address:", client_ip, "port:", client_port)
# 发送欢迎信息:  socket.send(string[, flags])
socket_conn.send(("Welcome!").encode())

while True:
    try:
        # 从client接收字符:  socket.recv(bufsize[, flags])
        data = socket_conn.recv(512)
        if len(data) > 0:
            print("received:", data)
            # 收到exit, 结束会话:
            if data.decode() == "exit":
                break
            # 否则, 回复给client相同的字符:
            socket_conn.send(data)
    except Exception:
        print("error!")
        socket_tcp.close()
        sys.exit(1)

# 关闭socket:  socket.close()
socket_conn.close()
socket_tcp.close()
