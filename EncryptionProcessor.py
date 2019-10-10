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
        self.filePath = '/nfs-dir/penelitian2019/'
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
            multi.get_CPU_Load()
            multi.get_RAM_Used()
            for response in multi():
                print(str(response))
                logging.debug(str(response))


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
        shl = subprocess.Popen("du -h " + self.filePath + self.rawFilePath + self.fileName, shell=True, stdout=subprocess.PIPE)
        stdout = shl.communicate()
        lim = stdout[0].find('\t')
        fileSize = stdout[0][0:lim]
        if fileSize[-1] is 'K':
            realFileSize = int(fileSize[0:-1]) * 1024
        elif fileSize[-1] is 'M':
            realFileSize = int(fileSize[0:-1]) * 1024 * 1024
        elif fileSize[-1] is 'G':
            realFileSize = int(fileSize[0:-1]) * 1024 * 1024 * 1024
        else:
            realFileSize = int(fileSize[0:-1])

        # print realFileSize
        splitSize = float(realFileSize) / float(len(self.workerIP))
        # print splitSize
        splitSize = int(round(splitSize))
        # print splitSize
        print('Start: Spliting File By Number of Workers')
        logging.debug('Start: Spliting File By Number of Workers')
        shl2 = subprocess.Popen("split -b " + str(splitSize) + " " + self.filePath + self.rawFilePath + self.fileName + " " + self.filePath + self.rawFilePath + self.fileName + ".",
                               shell=True, stdout=subprocess.PIPE)
        shl2.communicate()
        self.numPart = int(round(float(realFileSize)/float(splitSize)))
        print('Done: Spliting File By Number of Workers')
        logging.debug('Done: Spliting File By Number of Workers')
        print('File Splited Into ' + str(self.numPart) + ' Pieces')
        logging.debug('File Splited Into ' + str(self.numPart) + ' Pieces')
        print('Every Pieces Has ' + str(splitSize) + ' Size')
        logging.debug('Every Pieces Has ' + str(splitSize) + ' Size')

    def do_Encrypt(self):
        print('Start: Calling Worker To Encrypt Splitted Files')
        logging.debug('Start: Calling Worker To Encrypt Splitted Files')
        convThread = []
        fileNameToEnc = ''
        suffix = 'a'
        print suffix
        for idx in self.workerIP:
            fileNameToEnc = self.fileName + '.a' + suffix
            thread = EncryptThreads('Thread_a' + suffix, idx, fileNameToEnc, self.fileName)
            convThread.append(thread)
            suffix = chr(ord(suffix)+1)
            print suffix

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
        fileNameToDec = ''
        suffix = 'a'
        print suffix
        for idx in self.workerIP:
            fileNameToDec = self.fileName + '.a' + suffix
            thread = DecryptThreads('Thread_a' + suffix, idx, fileNameToDec, self.fileName)
            convThread.append(thread)
            suffix = chr(ord(suffix)+1)
            print suffix

        for j in convThread:
            j.start()

        for i in convThread:
            i.join()

        print('Done: Calling Worker To Decrypt Splitted Files')
        logging.debug('Done: Calling Worker To Decrypt Splitted Files')

    def do_MergeFile(self):
        print('Start: Merging Decrypted File')
        logging.debug('Start: Merging Decrypted File')
        #print("cat " + self.filePath + self.decryptedFilePath + self.fileName + ".?? > " + self.filePath + self.decryptedFilePath + self.fileName)
        shl = subprocess.Popen("cat " + self.filePath + self.decryptedFilePath + self.fileName + ".?? > " + self.filePath + self.decryptedFilePath + self.fileName, shell=True,
                               stdout=subprocess.PIPE)
        stdout = shl.communicate()
        print('Done: Merging Decypted Files')
        logging.debug('Done: Merging Decypted Files')