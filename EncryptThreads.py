import threading
import xmlrpclib
import logging

class EncryptThreads(threading.Thread):

    def __init__(self, threadID, idx, fileNameToEnc, fileName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.idx = idx
        self.fileNameToEnc = fileNameToEnc
        self.fileName = fileName

    def run(self):
        logging.debug('Starting %s', self.threadID)
        do_Encrypt(self.idx, self.fileNameToEnc, self.fileName)
        logging.debug('Exiting %s', self.threadID)


def do_Encrypt(idx, fileNameToEnc, fileName):
    # print idx
    # print fileNameToEnc
    # print fileName
    server = xmlrpclib.ServerProxy('http://' + idx + ':8000')
    multi = xmlrpclib.MultiCall(server)
    multi.do_EncryptFile(fileNameToEnc, fileName)
    for response in multi():
        print(response)
