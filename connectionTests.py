import socket
import re
from packetHandler import *
from packetClass import *

# SYN, SYN+ACK, ACK
def senderInit(sock, receiver_address, sender_address):

    packetObj = Packet(sender_address[1], 'localhost', 0, 0, "SYN", 0, "")
    packet = pickle.dumps(packetObj)
    sock.sendto(packet, receiver_address)
    received = sock.recv(4096)
    packetObj = pickle.loads(received)

   
    if packetObj.flag == "SYN+ACK":
        packetObj = Packet(sender_address[1], 'localhost', 0, 0, "ACK", 0, "")
        packet = pickle.dumps(packetObj)
        sock.sendto(packet, receiver_address)
        return True
    else:
        return False


def receiverInit(sock, port):

    received = sock.recv(4096)
    packetObj = pickle.loads(received)
    senderPort = packetObj.port
    if packetObj.flag == "SYN":
        packetObj = Packet(port, 'localhost', 0, 0, "SYN+ACK", 0, "")
        packet = pickle.dumps(packetObj)
        sock.sendto(packet, ('localhost', int(senderPort)))
        received = sock.recv(4096)
        packetObj = pickle.loads(received)
        if packetObj.flag == "ACK":
            return True
        else:
            return False



# FIN, ACK, FIN, ACK
def senderFinish(sock, receiver_address, sender_address):
    
    # Unsure if I need to add seq nums to these?



    packetObj = Packet(sender_address[1], 'localhost', 0, 0, "FIN", 0, "")
    packet = pickle.dumps(packetObj)
    sock.sendto(packet, receiver_address)

    received = sock.recv(4096)
    packetObj = pickle.loads(received)

    if packetObj.flag == "ACK":
        #wait for the servers FIN
        received = sock.recv(4096)
        packetObj = pickle.loads(received)

        if packetObj.flag == "FIN":
            #send final ACK and close
            packetObj = Packet(sender_address[1], 'localhost', 0, 0, "ACK", 0, "")
            packet = pickle.dumps(packetObj)
            sock.sendto(packet, receiver_address)
            print("Closing Connection")
            return False
        else:
            return True
    return True

def receiverFinish(sock, port, seqNum):
    # SEND THE ACK
    packetObj = Packet(port, 'localhost', 0, 0, "ACK", 0, "")
    packet = pickle.dumps(packetObj)
    sock.sendto(packet, ('localhost', int(port)+500))
    # SEND THE FIN
    packetObj = Packet(port, 'localhost', 0, 0, "FIN", 0, "")
    packet = pickle.dumps(packetObj)
    sock.sendto(packet, ('localhost',  int(port)+500))
    # GET THE FINAL ACK
    received = sock.recv(4096)
    packetObj = pickle.loads(received)
    if packetObj.flag == "ACK":
        print("Closing Connection")
        return False
    else: 
        return True

