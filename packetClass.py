class Packet:
    def __init__(self, port, senderAddr, seqNum, ackNum, flag, size, data):
        self.port = port
        self.senderAddr = senderAddr
        self.seqNum = seqNum
        self.ackNum = ackNum
        self.flag = flag
        self.size = size
        self.data = data

        self.checkSum = 1

    def checksum(self):
        print()
        # bleh

