#!/usr/bin/python3

import socket
import sys
import time
import operator

from packetHandler import *
from connectionTests import *
from fileReadWrite import *

receiver_port = int(sys.argv[1])
file_r = sys.argv[2]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', receiver_port)
sock.bind(server_address)

print('starting up on {} port {}'.format(*server_address))

#clearing the receiverlog file
fh=open("Receiver_log.txt", "w")
fh.write("{:^20} {:^20} {:^20} {:^20} {:^20} {:^20}\n".format("<event>", "<time>", "<type-of-packet>", "<seq-number>", "<number-of-bytes-data>", "<ack-number>"))
fh.close()

while True:

    print("waiting for connection attempt")
    connection, ackNum, start = receiverInit(sock, receiver_port)
    print("received conn")
    fileContents = []
    packetBuffer = []

    while connection:
        pickledPacket = sock.recv(4096)
        packetObj = pickle.loads(pickledPacket)
        # print("\npacket: \n    seqNum: {}\n    flag:{}".format(packetObj.seqNum, packetObj.flag))
        logReceiver(start, packetObj)
        
        # if packetObj.checksum != checksum():
        #     # discard
        #     print("packet corrupted, discarding")
        #     continue
        
        if packetObj.flag == "FIN":
            connection = receiverFinish(sock, receiver_port, packetObj.seqNum, start)  

        #  
        else:
 
            # print("curr ackNum:{}, packetSeqNum: {}".format(ackNum, packetObj.seqNum))
            if ackNum == packetObj.seqNum:
                # THIS MEANS PACKET ARRIVED AT RIGHT TIME AND ALL IS GOOD
                # ADD THE PACKET DATA TO FILE
                ackNum += packetObj.size
                fileContents.append(packetObj.data)

                # We we receive a correct packet search buffer for the next packet
                for packet in packetBuffer:
                    if packet.seqNum == ackNum:
                        ackNum += packet.size
                        fileContents.append(packetObj.data)
                        packetBuffer.remove(packet)


            else:# ackNum != packetObj.seqNum:
                #THE ARRIVED PACKET IS NOT THE RIGHT PACKET,
                print("not expecting this packet")
                
                if packetObj.seqNum > ackNum:
                    # Still waiting on another packet
                    # add to buffer
                    packetBuffer.append(packetObj)
                    packetBuffer = sorted(packetBuffer, key=operator.attrgetter('seqNum'))

                # elif packetObj.seqNUm < ackNum:

                    #we have already received this and dont do anything but ACK




            #ACK THAT A PACKET HAS ARRIVED, USING CURRENT ACKNUM
            ackPacket = ackGenerator(packetObj, ackNum)
            ackPacketObj = pickle.loads(ackPacket)
            sock.sendto(ackPacket ,('localhost', int(packetObj.port)))
            logReceiver(start, ackPacketObj)



    finalReceiverLog()
    fileWriter(file_r, fileContents)
    break


