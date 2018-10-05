#!/usr/bin/python3

import socket
import sys
from packetHandler import *
from connectionTests import *
from fileReadWrite import *
import re

receiver_port = int(sys.argv[1])
file_r = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', receiver_port)
sock.bind(server_address)

print('starting up on {} port {}'.format(*server_address))



while True:

    print("waiting for connection attempt")
    connection = receiverInit(sock, receiver_port)
    fileContents = []
    while connection == True:

        # print('\nwaiting to recieve message')
        pickledPacket = sock.recv(4096)
        packetObj = pickle.loads(pickledPacket)
        
        print("packet: \n    seqNum: {}\n    flag:{}".format(packetObj.seqNum, packetObj.flag))
        if packetObj.flag == "FIN":
            connection = receiverFinish(sock, receiver_port, packetObj.seqNum)  
        else:
            #Ack the packet and save the file
            ackResponse = sock.sendto(ackGenerator(packetObj.seqNum), ('localhost', int(packetObj.port)))
            fileContents.append(packetObj.data)
    # fileContents = bytes(fileContents, 'utf-8')        
    fileWriter("testWRITER.pdf", fileContents)



