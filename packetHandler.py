import re

def generatePackets(fileContents, maxSegSize):
    divider ='~!!!---!!!~'
    index = 0

    sequenceNumber = 0
    packetArray = [fileContents[i:i+maxSegSize] for i in range(0,len(fileContents), maxSegSize)]
    while index < len(packetArray):

        datagram = generateHeader(sequenceNumber, packetArray[index]) + divider + packetArray[index]
        packetArray[index] = bytes(datagram, 'utf-8')
        sequenceNumber += len(packetArray[index])
        index+=1

    return packetArray

def generateHeader(sequenceNumber, data):
    seqNumber = sequenceNumber
    typeOfPacket = "normal"
    ackNum = 0
    size = len(data)

    header = "seqNum:{}|ackNum:{}|typeOfPacket:{}|size:{}".format(seqNumber,ackNum,typeOfPacket,size)
    return header

def deconstructPacket(packet):
    
    divider = re.compile(r'~!!!---!!!~')
    
    packet = packet.decode('utf-8')
    packetHeader, packetData = divider.split(packet)
    return packetHeader, packetData

