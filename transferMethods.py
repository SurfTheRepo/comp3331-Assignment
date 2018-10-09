import pickle
import socket

import time
import signal

from timeout import *
from pldModule import * 
from fileReadWrite import *

def sendPackets(arrayOfPackets, receiver_address, sock, argv, start):

    estRTT = 0.5 
    devRTT = 0.25 
    gamma = float(argv[6])
    timeoutInterval = getTimeOutInterval(estRTT, devRTT, gamma)
    # timeoutInterval = 2
    seed = float(argv[14])
    random.seed(seed)

    i = 0

    for packet in arrayOfPackets:
        packetObj = pickle.loads(packet)
        # print('\nsending packet #{}, seqNum: {}'.format(i, packetObj.seqNum))
        i+=1
        status = sendPacketPLD(random.random(), sock, packet, receiver_address, argv)
        logSender(start, packetObj)
        print("   PLDoutput:", status)

        while True:
            try:
                with Timeout(timeoutInterval): 

                    received = sock.recv(4096)
                    ackObject = pickle.loads(received)
                    logSender(start, ackObject)
                    # print("ack:{}".format(ackObject.ackNum))

                    if ackObject.ackNum < packetObj.seqNum + packetObj.size:
                        print("already received this")
                        # need to deal with what to do if recieve a ack we aleady have


                    if ackObject.ackNum > packetObj.seqNum + packetObj.size:
                        
                        print(ackObject.ackNum, "<-- ack, seqNum+size --> ",packetObj.seqNum + packetObj.size )
                        print("{} not received.".format(packetObj.seqNum))

                        # needa do logic for what to do if missing an ack
                    
                    break
            except Timeout.Timeout:
                print("didnt receive ack in time, need to resend packet")


def getTimeOutInterval(estRTT, devRTT, gamma):
    return estRTT +gamma *devRTT


