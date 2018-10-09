import re
import pickle
from packetClass import *


   
def generatePackets(fileContents, sender_address, sequenceNumber):

    

    pickledPacketArray = []
    for packet in fileContents:
        packetObj = Packet(sender_address[1], 'localhost', sequenceNumber, 0, 'Data', len(packet), packet)
        pickledPacket = pickle.dumps(packetObj)
        pickledPacketArray.append(pickledPacket)
        # print(len(pickledPacket))
        sequenceNumber +=len(packet)

    return pickledPacketArray


def ackGenerator(receivedPacketObj, ackNum):

    packetObj = Packet(receivedPacketObj.port, 'localhost', 0, ackNum, "ACK", 0, "")
    packet = pickle.dumps(packetObj)

    return packet
