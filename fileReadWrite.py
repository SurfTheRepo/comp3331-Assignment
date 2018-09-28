

def fileReader(fileName):
    # Read file and return the contents in a byte utf-8 format
    fh = open(fileName, "rb")
    fileContents = ''
    for line in fh:
        fileContents += str(line)
    fh.close()
    # print(fileContents)

    # fileWriter("testWriter.pdf", fileContents)
    return fileContents
        

def fileWriter(fileName, contents):
    fh = open(fileName, "w")
    for line in contents:
        fh.write(line)
    fh.close()

