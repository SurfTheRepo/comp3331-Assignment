#!/usr/bin/python3

import socket
import sys
from fileReadWrite import fileReader
from packetHandler import generatePackets

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
server_address = (receiver_host_ip, receiver_port)

#getting content from pdf
fileContents = fileReader(fileName)

# turning content into packets
arrayOfPackets = generatePackets(fileContents, maxSegSize)

i = 0
for packet in arrayOfPackets:

    print('sending packet num {}'.format(i))
    sent = sock.sendto(packet, server_address)
    i+=1

    # print('waiting to receive')
    # data, server = sock.recvfrom(4096)
    # print('received {!r}'.format(data))

print('closing socket')
sock.close()