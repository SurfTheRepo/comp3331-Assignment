#!/usr/bin/python3

import socket
import sys
from packetHandler import deconstructPacket


receiver_port = int(sys.argv[1])
file_r = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', receiver_port)
sock.bind(server_address)

print('starting up on {} port {}'.format(*server_address))

while True:
    print('\nwaiting to recieve message')
    packet, address = sock.recvfrom(4096)

    #turning packet into data
    header, data = deconstructPacket(packet)
    # print("header:{} \n headersize:{}".format( header, len(bytes(header,'utf-8'))))
    print("header:", header)
    print("data:", data)


    

