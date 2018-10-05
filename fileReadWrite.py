# import codecs

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

