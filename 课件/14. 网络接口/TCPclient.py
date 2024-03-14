#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import time
import sys

# client program
print ('######################### TCP client #########################')

# server's IP address and port:
HOST_IP = '192.168.2.112'
HOST_PORT = 50007

# create socket object:
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

i = 0
while True:
    try:
        # connect to server:
        print ('connecting to server...')
        socket_tcp.connect((HOST_IP, HOST_PORT))
        break
    except Exception:
        print ('fail, retry later...')
        i += 1
        if i == 5:
            print ('fail!')
            sys.exit(1)
        time.sleep(1)
        continue
print ('succeed!')

# receive welcome from server:
data_recv = socket_tcp.recv(512)
print ('received:', data_recv.decode())

while True:
    try:
        data_send = input('message to send: ')
        # send data to server:
        socket_tcp.send(data_send.encode())
        if data_send == 'exit':
            break
        # receive echo from server:
        data_recv = socket_tcp.recv(512)
        print ('received:', data_recv.decode())
    except Exception:
        print ('error!')
        socket_tcp.close()
        sys.exit(1)
    
# close socket:
socket_tcp.close()
