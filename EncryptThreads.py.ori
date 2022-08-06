import threading
import xmlrpclib
import logging

class EncryptThreads(threading.Thread):

    def __init__(self, threadID, idx, startPart, endPart, fileName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.idx = idx
        self.startPart = startPart
        self.endPart = endPart
        self.fileName = fileName

    def run(self):
        logging.debug('Starting %s', self.threadID)
        do_Encrypt(self.idx, self.startPart, self.endPart, self.fileName)
        logging.debug('Exiting %s', self.threadID)


def do_Encrypt(idx, startPart, endPart, fileName):
    server = xmlrpclib.ServerProxy('http://' + idx + ':8000')
    multi = xmlrpclib.MultiCall(server)
    multi.do_EncryptFile(startPart, endPart, fileName)
    for response in multi():
        print(response)
