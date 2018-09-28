#!/usr/bin/python3

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 8888)
message = b'this is the message. it will be repeated.'

try:
	print('sending {!r}'.format(message))
	sent = sock.sendto(message, server_address)
finally:
	print('closing socket')
	sock.close()