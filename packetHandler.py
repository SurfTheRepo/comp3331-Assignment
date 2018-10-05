import re
import pickle
from packetClass import *


   
def generatePackets(fileContents, sender_address):

    sequenceNumber = 0

    pickledPacketArray = []
    for packet in fileContents:
        packetObj = Packet(sender_address[1], 'localhost', sequenceNumber, 0, 'normal', len(packet), packet)
        pickledPacket = pickle.dumps(packetObj)
        pickledPacketArray.append(pickledPacket)
        print(len(pickledPacket))
        sequenceNumber +=len(packet)

    return pickledPacketArray




def ackGenerator(seqNum):
    return bytes("ack:{}".format(seqNum), 'utf-8')
