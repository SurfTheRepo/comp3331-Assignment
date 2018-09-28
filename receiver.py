#!/usr/bin/python3

import socket
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


server_address = ('localhost', 8888)
print('startig up on {} port {}'.format(*server_address))

sock.bind(server_address)



while True:
	print('\nwaiting to recieve message')
	data, address = sock.recvfrom(4096)

	print('received {} bytes from {}'.format(len(data), address))
	print(data)
