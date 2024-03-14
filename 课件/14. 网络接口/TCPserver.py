#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys

# server program
print ('######################### TCP server #########################')

# server's IP address and port:
HOST_IP = '192.168.2.109'
HOST_PORT = 50007

# create socket object:
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind socket to address:
socket_tcp.bind((HOST_IP, HOST_PORT))
# listen for connections:
socket_tcp.listen(1)
print ('listen @ IP address:', HOST_IP, 'port:' ,HOST_PORT)

# accept a connection:
socket_conn, (client_ip, client_port) = socket_tcp.accept()
print ('connected by: IP address:', client_ip, 'port:', client_port)
# send welcome to client:
socket_conn.send(('Welcome!').encode())

while True:
    try:
        # receive data from client:
        data = socket_conn.recv(512)
        if len(data) > 0:
            print ('received:', data.decode())
            if data.decode() == 'exit':
                break
            # send echo to client:
            socket_conn.send(data)
    except Exception:
        print ('error!')
        socket_tcp.close()
        sys.exit(1)

# close socket:
socket_conn.close()
socket_tcp.close()