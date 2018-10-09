import socket
import re
import time
from packetHandler import *
from packetClass import *
from fileReadWrite import *

# SYN, SYN+ACK, ACK
def senderInit(sock, receiver_address, sender_address):
    print("attempting to connect..........")
    start = time.time()
    packetObj = Packet(sender_address[1], 'localhost', 0, 0, "SYN", 0, "")
    packet = pickle.dumps(packetObj)
    sock.sendto(packet, receiver_address)
    logSender(start, packetObj)

    received = sock.recv(4096)
    packetObj = pickle.loads(received)
    logSender(start, packetObj)

    if packetObj.flag == "SYN+ACK":
        packetObj = Packet(sender_address[1], 'localhost', 0, 0, "ACK", 0, "")
        packet = pickle.dumps(packetObj)
        sock.sendto(packet, receiver_address)
        logSender(start, packetObj)
        print("connection succesful")
        print("Sending from Address:", sender_address)
        return True, start
    else:
        return False


def receiverInit(sock, port):
    received = sock.recv(4096)
    start = time.time()
    packetObj = pickle.loads(received)
    logReceiver(start, packetObj)
    senderPort = packetObj.port
    if packetObj.flag == "SYN":
        packetObj = Packet(port, 'localhost', 0, 0, "SYN+ACK", 0, "")
        packet = pickle.dumps(packetObj)
        sock.sendto(packet, ('localhost', int(senderPort)))
        logReceiver(start, packetObj)
        received = sock.recv(4096)
        packetObj = pickle.loads(received)
        logReceiver(start, packetObj)
        if packetObj.flag == "ACK":
            return True, packetObj.seqNum, start
        else:
            return False



# FIN, ACK, FIN, ACK
def senderFinish(sock, receiver_address, sender_address, start):
    
    # Unsure if I need to add seq nums to these?
    packetObj = Packet(sender_address[1], 'localhost', 0, 0, "FIN", 0, "")
    packet = pickle.dumps(packetObj)
    sock.sendto(packet, receiver_address)
    logSender(start, packetObj)

    received = sock.recv(4096)
    packetObj = pickle.loads(received)
    logSender(start, packetObj)

    if packetObj.flag == "ACK":
        #wait for the servers FIN
        received = sock.recv(4096)
        packetObj = pickle.loads(received)
        logSender(start, packetObj)

        if packetObj.flag == "FIN":
            #send final ACK and close
            packetObj = Packet(sender_address[1], 'localhost', 0, 0, "ACK", 0, "")
            packet = pickle.dumps(packetObj)
            sock.sendto(packet, receiver_address)
            logSender(start, packetObj)
            print("Closing Connection")
            return False
        else:
            print(packetObj.flag)
            print("ofuq")
            return True
    return True

def receiverFinish(sock, port, seqNum, start):
    # SEND THE ACK
    packetObj = Packet(port, 'localhost', 0, 0, "ACK", 0, "")
    packet = pickle.dumps(packetObj)
    sock.sendto(packet, ('localhost', int(port)+500))
    logReceiver(start, packetObj)
    # SEND THE FIN
    packetObj = Packet(port, 'localhost', 0, 0, "FIN", 0, "")
    packet = pickle.dumps(packetObj)
    sock.sendto(packet, ('localhost',  int(port)+500))
    logReceiver(start, packetObj)
    # GET THE FINAL ACK
    received = sock.recv(4096)
    packetObj = pickle.loads(received)
    logReceiver(start, packetObj)
    if packetObj.flag == "ACK":
        print("Closing Connection")
        return False
    else: 
        return True

