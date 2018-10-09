#!/usr/bin/python3

import socket
import sys
import random

from fileReadWrite import *
from packetHandler import *
from connectionTests import *
from transferMethods import *

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
seed = sys.argv[14] 

random.seed(seed)

# clearing send_log.txt
fh = open("Sender_log.txt", "w")
fh.write("{:^20} {:^20} {:^20} {:^20} {:^20} {:^20}\n".format("<event>", "<time>", "<type-of-packet>", "<seq-number>", "<number-of-bytes-data>", "<ack-number>"))
fh.close()
#Setting up correct UDP socket & ports etc...
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_address = (receiver_host_ip, receiver_port)

#setting up address for receiving ACKS
sender_address = ('localhost', receiver_port+500)
sock.bind(sender_address)


#getting content from pdf
fileContents = fileReader(fileName, maxSegSize)

# turning content into packets
# sequenceNumber = random.randint(0,2**32)
sequenceNumber = 0

arrayOfPackets = generatePackets(fileContents, sender_address, sequenceNumber)



#starting connection
connection, start = senderInit(sock, receiver_address, sender_address,)
if connection:


    print("Sending file {}, of size {} to {}".format(fileName, sys.getsizeof(fileContents), receiver_address))
    
 
    sendPackets(arrayOfPackets, receiver_address, sock, sys.argv, start)

    connection = senderFinish(sock, receiver_address, sender_address, start)
    
    finalSenderLog()
else:
    print("failure to connect")

print('closing socket')
sock.close()


