import random
import time

def sendPacketPLD(randomNum, sock, packet, receiver_address, argv):

    pDrop = float(argv[7])
    pDuplicate = float(argv[8])
    pCorrupt = float(argv[9])
    pOrder = float(argv[10])
    # print(argv[11])
    maxOrder = int(argv[11])
    pDelay = float(argv[12])
    maxDelay = int(argv[13])
    seed = float(argv[14])

    random.seed(randomNum)


    if random.random() < pDrop:
        return "drop"

    # deal with dropped packets first

    # elif random.random() < pDuplicate:
    #     sock.sendto(packet, receiver_address)
    #     sock.sendto(packet, receiver_address)
    #     return "duplicate"
    # elif random.random() < pCorrupt:
    #     #flip a bit donno how
    #     sock.sendto(packet, receiver_address)
    #     return "corrupt"
    # elif random.random() < pOrder:
    #     #some how save packet, and wait for # of packets to send then send this one
    #     return "order"
    # elif random.random() < pDelay:
    #     # print("delay")
    #     # START ANOTHER TRHEAD FOR THE DELAY 
    
    #     time.sleep(random.randint(0, maxDelay))
    #     sock.sendto(packet, receiver_address)
    #     return "delay"
    else:
        sock.sendto(packet, receiver_address)
        return "send"        
