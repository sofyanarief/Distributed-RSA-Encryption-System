import logging
import subprocess
import xmlrpclib
from Crypto.PublicKey import RSA

from EncryptThreads import EncryptThreads
from DecryptThreads import DecryptThreads

logging.basicConfig(filename='broker_run.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

class EncryptionProcessor:
    def __init__(self):
        print('Initializing System')
        logging.debug('Initializing System')
        self.workerIP = []
        self.workerRes = []
        self.filePath = '/home/engine/PycharmProjects/Distributed-RSA-Encryption-System/'
        self.fileName = ''
        self.jobToHandle = []
        self.rawFilePath = 'raw-file/'
        self.keyFilePath = 'key-file/'
        self.encryptedFilePath = 'enc-file/'
        self.decryptedFilePath = 'dec-file/'
        self.keySize = 128
        self.numPart = 0
        print('System Initialized')
        logging.debug('System Initialized')

    def set_workerIP(self, param):
        print('Setting Worker IP: ' + str(param))
        logging.debug('Setting Worker IP: ' + str(param))
        self.workerIP = param

    def set_fileName(self, fileName):
        print('Setting File To Process: ' + fileName)
        logging.debug('Setting File To Process : ' + fileName)
        self.fileName = fileName

    def set_keySize(self, keySize):
        print('Setting Key Size: ' + str(keySize))
        logging.debug('Setting Key Size: ' + str(keySize))
        self.keySize = keySize

    def get_AllWorkerRes(self):
        print('Getting All Worker Resources')
        logging.debug('Getting All Worker Resources')
        for idx in self.workerIP:
            server = xmlrpclib.ServerProxy('http://' + idx + ':8000')
            multi = xmlrpclib.MultiCall(server)
            # multi.get_CPU_Load()
            # multi.get_RAM_Used()
            multi.get_CPU_CoreNum()
            respool = []
            for response in multi():
                respool.append(response)
            self.workerRes.append(respool)
        self.print_AllWorkerResource()

    def print_AllWorkerResource(self):
        print('Printing All Worker Resources')
        logging.debug('Printing All Worker Resources')
        for i in range(len(self.workerRes)):
            print('Worker ' + repr(i + 1) + ':')
            logging.debug('Worker ' + repr(i + 1) + ':')
            for j in range(len(self.workerRes[i])):
                print self.workerRes[i][j]

    def do_GenerateKeyForFile(self):
        print('Start: Generating Public And Private Key')
        logging.debug('Start: Generating Public And Private Key')
        newKey = RSA.generate(self.keySize, e=65537)
        private_key = newKey.exportKey("PEM")
        public_key = newKey.publickey().exportKey("PEM")
        print('Done: Generating Public And Private Key --')
        logging.debug('Done: Generating Public And Private Key')

        print('Start: Writing Private Key To File')
        logging.debug('Start: Writing Private Key To File')
        # print(private_key)
        # logging.debug(private_key)
        fd = open(self.filePath + self.keyFilePath + "priv" + self.fileName + ".pem", "wb")
        fd.write(private_key)
        fd.close()
        print('Done: Writing Private Key To File')
        logging.debug('Done: Writing Private Key To File')

        print('Start: Writing Public Key To File')
        logging.debug('Start: Writing Public Key To File')
        # print(public_key)
        # logging.debug(public_key)
        fd = open(self.filePath + self.keyFilePath + "pub" + self.fileName + ".pem", "wb")
        fd.write(public_key)
        fd.close()
        print('Done: Writing Public Key To File')
        logging.debug('Done: Writing Public Key To File')

    def do_SplitFile(self):
        print('Getting File Size')
        logging.debug('Getting File Size')
        shl = subprocess.Popen("du -h " + self.filePath + self.rawFilePath + self.fileName, shell=True,
                               stdout=subprocess.PIPE)
        stdout = shl.communicate()
        lim = stdout[0].find('\t')
        fileSize = stdout[0][0:lim]
        if fileSize[-1] is 'K':
            realFileSize = int(fileSize[0:-1]) * 1024
        elif fileSize[-1] is 'M':
            realFileSize = int(fileSize[0:-1]) * 1024 * 1024
        else:
            realFileSize = int(fileSize[0:-1])
        # print realFileSize

        splitSize = self.keySize / 8
        # print splitSize

        if realFileSize % splitSize != 0:
            self.numPart = (realFileSize / splitSize) + 1
        else:
            self.numPart = (realFileSize / splitSize)
        # print self.numPart

        print('Start: Spliting File By Block Size')
        logging.debug('Start: Spliting File By Block Size')
        shl2 = subprocess.Popen("split -b " + str(
            splitSize) + " " + self.filePath + self.rawFilePath + self.fileName + " " + self.filePath + self.rawFilePath + self.fileName + ". -da 7",
                                shell=True, stdout=subprocess.PIPE)
        shl2.communicate()
        print('Done: Spliting File By Number of Workers')
        logging.debug('Done: Spliting File By Number of Workers')
        print('File Splited Into ' + str(self.numPart) + ' Pieces')
        logging.debug('File Splited Into ' + str(self.numPart) + ' Pieces')
        print('Every Pieces Has ' + str(splitSize) + ' Size')
        logging.debug('Every Pieces Has ' + str(splitSize) + ' Size')

    def do_CalculateJobAllocation(self):
        print('Calculate Job Allocation')
        logging.debug('Calculate Job Allocation')
        curRes = []
        totalCurRes = 0
        for i in range(len(self.workerRes)):
            # curCPU = 0.7 * (1 - (float(self.workerRes[i][0]) / 100)) * (4 / 0.5)
            # curRAM = (1 - 0.3) * (1 - (float(self.workerRes[i][1]) / 100)) * (1024 / 256)
            curCPUCore = self.workerRes[i][0]
            curRes.append(curCPUCore)
            # curRes.append(curCPU + curRAM)
            totalCurRes = totalCurRes + curRes[i]
        maxCurRes = max(curRes)
        # print totalCurRes
        # print maxCurRes
        idxMaxRes = 0
        for j in range(len(self.workerRes)):
            if curRes[j] == maxCurRes:
                idxMaxRes = j
            self.jobToHandle.append(int(round(curRes[j] / totalCurRes * self.numPart)))
            # print self.jobToHandle[j]
        self.jobToHandle[idxMaxRes] = self.jobToHandle[idxMaxRes] + (self.numPart - sum(self.jobToHandle))
        # print self.jobToHandle

    def do_Encrypt(self):
        print('Start: Calling Worker To Encrypt Splitted Files')
        logging.debug('Start: Calling Worker To Encrypt Splitted Files')
        convThread = []
        i = 0
        startPart = 0
        for idx in self.workerIP:
            print idx
            print 'start : ' + str(startPart)
            endPart = startPart + self.jobToHandle[i] - 1
            print 'end : ' + str(endPart)
            thread = EncryptThreads('Thread_' + str(i), idx, startPart, endPart, self.fileName)
            convThread.append(thread)
            startPart = endPart + 1
            i += 1

        for j in convThread:
            j.start()

        for i in convThread:
            i.join()
        print('Done: Calling Worker To Encrypt Splitted Files')
        logging.debug('Done: Calling Worker To Encrypt Splitted Files')

    def do_Decrypt(self):
        print('Start: Calling Worker To Decrypt Splitted Files')
        logging.debug('Start: Calling Worker To Decrypt Splitted Files')
        convThread = []
        i = 0
        startPart = 0
        for idx in self.workerIP:
            print idx
            print 'start : ' + str(startPart)
            endPart = startPart + self.jobToHandle[i] - 1
            print 'end : ' + str(endPart)
            thread = DecryptThreads('Thread_' + str(i), idx, startPart, endPart, self.fileName)
            convThread.append(thread)
            startPart = endPart + 1
            i += 1

        for j in convThread:
            j.start()

        for i in convThread:
            i.join()

        print('Done: Calling Worker To Decrypt Splitted Files')
        logging.debug('Done: Calling Worker To Decrypt Splitted Files')

    def do_MergeFile(self):
        print('Start: Merging Decrypted File')
        logging.debug('Start: Merging Decrypted File')
        # print("cat " + self.filePath + self.decryptedFilePath + self.fileName + ".?? > " + self.filePath + self.decryptedFilePath + self.fileName)
        shl = subprocess.Popen(
            "cat " + self.filePath + self.decryptedFilePath + self.fileName + ".* > " + self.filePath + self.decryptedFilePath + self.fileName,
            shell=True,
            stdout=subprocess.PIPE)
        stdout = shl.communicate()
        print('Done: Merging Decypted Files')
        logging.debug('Done: Merging Decypted Files')