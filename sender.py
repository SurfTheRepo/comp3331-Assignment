#!/usr/bin/python3

import socket
import sys
from fileReadWrite import fileReader
from packetHandler import generatePackets
from connectionTests import *
 

receiver_host_ip = sys.argv[1]
receiver_port = int(sys.argv[2])
fileName = sys.argv[3]
maxWindowSize = int(sys.argv[4])
maxSegSize = int(sys.argv[5])
gamma = int(sys.argv[6])
# The following 8 arguments are used exclusively by the PLD module
# pDrop = sys.argv[7]
# pDuplicate = sys.argv[8]
# pCorrupt = sys.argv[9]
# pOrder = sys.argv[10]
# maxOrder = sys.argv[11]
# pDelay = sys.argv[12]
# maxDelay = sys.argv[13]
# seed = sys.argv[14] 

#Setting up correct UDP socket & ports etc...
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_address = (receiver_host_ip, receiver_port)

#setting up address for receiving ACKS
sender_address = ('localhost', receiver_port+500)
sock.bind(sender_address)



#getting content from pdf
fileContents = fileReader(fileName)

# turning content into packets
arrayOfPackets = generatePackets(fileContents, maxSegSize, sender_address)



#starting connection
print("attempting to connect..........")
connection = senderInit(sock, receiver_address, sender_address)
if connection:
    print("connection succesful")
    print("Sending from Address:", sender_address)
    print("Sending file {}, of size {} to {}".format(fileName, len(fileContents), receiver_address))
    
    i = 0
    for packet in arrayOfPackets:

        print('sending packet #{}'.format(i))
        sent = sock.sendto(packet, receiver_address)
        i+=1

        received = sock.recv(4096)
        print(received)


    connection = senderFinish(sock, receiver_address, sender_address)
else:
    print("failure to connect")

print('closing socket')
sock.close()