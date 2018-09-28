import re



def generatePackets(fileContents, maxSegSize, sender_address):
    divider = bytes('~!!!---!!!~', 'utf-8')
    index = 0

    fileContents = bytes(fileContents, 'utf-8')
    sequenceNumber = 0
    packetArray = [fileContents[i:i+maxSegSize] for i in range(0,len(fileContents), maxSegSize)]
    while index < len(packetArray):

        sequenceNumber += len(packetArray[index])
        packetArray[index] = generateHeader(sequenceNumber, packetArray[index], sender_address) + divider + packetArray[index]
        index+=1
    return packetArray



def generateHeader(sequenceNumber, data, sender_address):
    seqNumber = sequenceNumber
    typeOfPacket = "normal"
    ackNum = 0
    size = len(data)


    header = "port:{}|seqNum:{}|ackNum:{}|typeOfPacket:{}|size:{}".format(sender_address[1],seqNumber,ackNum,typeOfPacket,size)
    return bytes(header, 'utf-8')



def headerHandler(header):
    m = re.search(r'port:(\d+)\|seqNum:(\d+)\|ackNum:(\d+)\|typeOfPacket:([a-zA-Z]+)\|size:(\d+)',header)
    port =m.group(1)
    seqNum = m.group(2)
    # ackNum = m.group(3)
    typeOfPacket = m.group(4)
    size = m.group(5)

    print("port:{}\nseqNum:{}\ntype:{}\nsize:{}\n".format(port,seqNum,typeOfPacket,size))

    return port, seqNum, typeOfPacket



def deconstructPacket(packet):
    
    divider = re.compile(r'~!!!---!!!~')
    
    packet = packet.decode('utf-8')
    packetHeader, packetData = divider.split(packet)
    return packetHeader, packetData

def ackGenerator(seqNum):
    return bytes("ack:{}".format(seqNum), 'utf-8')
