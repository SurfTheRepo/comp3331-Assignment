import socket
import re
from packetHandler import *


# SYN, SYN+ACK, ACK
def senderInit(sock, receiver_address, sender_address):

    packet = bytes("port:{}|seqNum:{}|ackNum:{}|typeOfPacket:{}|size:{}~!!!---!!!~".format(sender_address[1], 0, 0, "SYN", 0), 'utf-8')
    sock.sendto(packet, receiver_address)
    received = sock.recv(4096)
    header = deconstructPacket(received)[0]
    m = re.search(r'.*typeOfPacket:([a-zA-Z]+\+[a-zA-Z]+).*', header)
    if m.group(1) == "SYN+ACK":
        sock.sendto(bytes("port:{}|seqNum:{}|ackNum:{}|typeOfPacket:{}|size:{}~!!!---!!!~".format(sender_address[1], 0, 0, "ACK", 0), 'utf-8'), receiver_address)
        return True
    else:
        return False


def receiverInit(sock, port):

    received = sock.recv(4096)
    header = deconstructPacket(received)[0]
    m = re.search(r'port:(\d+).*typeOfPacket:([a-zA-Z]+)', header)
    if m.group(2) == "SYN":
        packet = bytes("port:{}|seqNum:{}|ackNum:{}|typeOfPacket:{}|size:{}~!!!---!!!~".format(port, 0, 0, "SYN+ACK", 0), 'utf-8')
        sock.sendto(packet, ('localhost', int(m.group(1))))
        received = sock.recv(4096)
        header = deconstructPacket(received)[0]
        m = re.search(r'typeOfPacket:([a-zA-Z]+)', header)
        if m.group(1) == "ACK":
            return True
        else:
            return False



# FIN, ACK, FIN, ACK
def senderFinish(sock, receiver_address, sender_address):
    
    # Unsure if I need to add seq nums to these?

    packet = bytes("port:{}|seqNum:{}|ackNum:{}|typeOfPacket:{}|size:{}~!!!---!!!~".format(sender_address[1], 0, 0, "FIN", 0), 'utf-8')
    sock.sendto(packet, receiver_address)
    received = sock.recv(4096)
    header = deconstructPacket(received)[0]
    m = re.search(r'.*typeOfPacket:([a-zA-Z]+).*', header)
    if m.group(1) == "ACK":
        #wait for the servers FIN
        received = sock.recv(4096)
        header = deconstructPacket(received)[0]
        m = re.search(r'.*typeOfPacket:([a-zA-Z]+).*', header)
        if m.group(1) == "FIN":
            #send final ACK and close
            packet = bytes("port:{}|seqNum:{}|ackNum:{}|typeOfPacket:{}|size:{}~!!!---!!!~".format(sender_address[1], 0, 0, "ACK", 0), 'utf-8')
            sock.sendto(packet, receiver_address)
            print("Closing Connection")
            return False
        else:
            return True
    return True

def receiverFinish(sock, port):
    # SEND THE ACK
    packet = bytes("port:{}|seqNum:{}|ackNum:{}|typeOfPacket:{}|size:{}~!!!---!!!~".format(port, 0, 0, "ACK", 0), 'utf-8')
    sock.sendto(packet, ('localhost', int(port)+500))
    # SEND THE FIN
    packet = bytes("port:{}|seqNum:{}|ackNum:{}|typeOfPacket:{}|size:{}~!!!---!!!~".format(port, 0, 0, "FIN", 0), 'utf-8')
    sock.sendto(packet, ('localhost',  int(port)+500))
    # GET THE FINAL ACK
    received = sock.recv(4096)
    header = deconstructPacket(received)[0]
    m = re.search(r'typeOfPacket:([a-zA-Z]+)', header)
    if m.group(1) == "ACK":
        print("Closing Connection")
        return False
    else: 
        return True

