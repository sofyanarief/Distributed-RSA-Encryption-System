import threading
import xmlrpclib
import logging

class DecryptThreads(threading.Thread):

    def __init__(self, threadID, idx, startPart, endPart, fileName, keyName):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.idx = idx
        self.startPart = startPart
        self.endPart = endPart
        self.fileName = fileName
        self.keyName = keyName

    def run(self):
        logging.debug('Starting %s', self.threadID)
        do_Decrypt(self.idx, self.startPart, self.endPart, self.fileName, self.keyName)
        logging.debug('Exiting %s', self.threadID)


def do_Decrypt(idx, startPart, endPart, fileName, keyName):
    server = xmlrpclib.ServerProxy('http://' + idx + ':8000')
    multi = xmlrpclib.MultiCall(server)
    multi.do_DecryptFile(startPart, endPart, fileName, keyName)
    for response in multi():
        print(response)
