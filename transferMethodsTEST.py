import pickle
import socket

import time
import signal

from timeout import *
from pldModule import * 
from fileReadWrite import *

def sendPackets(listOfPackets, receiver_address, sock, argv, start):

    estRTT = 0.5 
    devRTT = 0.25 
    gamma = float(argv[6])
    seed = float(argv[14])
    maxWindowSize = int(argv[4])

    random.seed(seed)

    lastByteSent = 0
    lastByteAcked = 0
    # timeoutInterval = getTimeOutInterval(estRTT, devRTT, gamma)
    # timeoutInterval = 2

    lastPacketAcked = 0

    packetIterator = iter(listOfPackets)

    while lastByteSent - lastByteAcked <= maxWindowSize:
                


            



    



    


# def getTimeOutInterval(estRTT, devRTT, gamma):
#     return estRTT +gamma *devRTT


