# import codecs
import time

def fileReader(fileName, size):
    # Read file and return the contents in a byte utf-8 format
    fh = open(fileName, "rb")
    l = fh.read(size)

    fileContents = []
    while(l):
        # print("packet = ", l)
        fileContents.append(l)
        l = fh.read(size)
    return fileContents
        

def fileWriter(fileName, contents):
    fh = open(fileName, "wb")
    for line in contents:
        fh.write(line)
    fh.close()

def logReceiver(start, packetObj):

#     <event> <time> <type-of-packet> <seq-number> <number-of-bytes-data> <ack-number> 
    event = "placeholder"
    currTime = "%.3f" % (time.time() - start)
    typeOfPacket = packetObj.flag
    seqNum = packetObj.seqNum
    number_of_byte = packetObj.size
    ackNum = packetObj.ackNum
    info = "{:^20} {:^20} {:^20} {:^20} {:^20} {:^20}".format(event, currTime, typeOfPacket, seqNum, number_of_byte, ackNum) 
    transmissionLogger("Receiver_log.txt", info)

def logSender(start, packetObj):

    event = "placeholder"
    currTime = "%.3f" % (time.time() - start)
    typeOfPacket = packetObj.flag
    seqNum = packetObj.seqNum
    number_of_byte = packetObj.size
    ackNum = packetObj.ackNum
    info = "{:^20} {:^20} {:^20} {:^20} {:^20} {:^20} ".format(event, currTime, typeOfPacket, seqNum, number_of_byte, ackNum) 
    transmissionLogger("Sender_log.txt", info)


def finalSenderLog():
    fh = open("Sender_log.txt", "a")
    fh.write("\n\n")
    fh.write("Size of the file (in Bytes) = {}\n".format("XXX"))
    fh.write("Number of Segments handled by PLD = {}\n".format("XXX"))
    fh.write("Number of Segments Dropped = {}\n".format("XXX"))
    fh.write("Number of Segments Corrupted  = {}\n".format("XXX"))
    fh.write("Number of Segments Re-ordered  = {}\n".format("XXX"))
    fh.write("Number of Segments Duplicated  = {}\n".format("XXX"))
    fh.write("Number of Segments Delayed  = {}\n".format("XXX"))
    fh.write("Number of Retransmissions due to timeout = {}\n".format("XXX"))
    fh.write("Number of Fast Retransmissions = {}\n".format("XXX"))
    fh.write("Number of Duplicate Acknowledgements received = {}\n".format("XXX"))

def finalReceiverLog():
    fh = open("Receiver_log.txt", "a")
    fh.write("\n\n")
    fh.write("Amount of Data Received (bytes)  = {}\n".format("XXX"))
    fh.write("Total segments received = {}\n".format("XXX"))
    fh.write("Data segments received = {}\n".format("XXX"))
    fh.write("Data Segments with bit errors  = {}\n".format("XXX"))
    fh.write("Duplicate data segments received  = {}\n".format("XXX"))
    fh.write("Duplicate Acks sent = {}\n".format("XXX"))


def transmissionLogger(file, info):
    fh = open(file, "a")
    fh.write(info)
    fh.write("\n")
    fh.close()
