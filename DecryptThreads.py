import threading
import xmlrpclib
import logging

class DecryptThreads(threading.Thread):

    def __init__(self, threadID, idx, fileNameToDec, fileName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.idx = idx
        self.fileNameToDec = fileNameToDec
        self.fileName = fileName

    def run(self):
        logging.debug('Starting %s', self.threadID)
        do_Decrypt(self.idx, self.fileNameToDec, self.fileName)
        logging.debug('Exiting %s', self.threadID)


def do_Decrypt(idx, fileNameToDec, fileName):
    # print idx
    # print fileNameToEnc
    # print fileName
    server = xmlrpclib.ServerProxy('http://' + idx + ':8000')
    multi = xmlrpclib.MultiCall(server)
    multi.do_DecryptFile(fileNameToDec, fileName)
    for response in multi():
        print(response)
