import threading
import time

from EncryptionProcessor import EncryptionProcessor

if __name__ == '__main__':
    print('---- System Starting ----')
    encryptionProcessor = EncryptionProcessor()
    # encryptionProcessor.set_fileName('1mb-file.txt')
    encryptionProcessor.set_fileName('16kb-file.txt')
    encryptionProcessor.set_keySize(4096)
    encryptionProcessor.do_GenerateKeyForFile()
    # time.sleep(5)
    encryptionProcessor.set_workerIP(['192.168.60.181', '192.168.60.182', '192.168.60.183', '192.168.60.184', '192.168.60.185'])
    # encryptionProcessor.set_workerIP(['192.168.60.183', '192.168.60.184', '192.168.60.185'])
    # encryptionProcessor.set_workerIP(['192.168.60.180'])
    # encryptionProcessor.get_AllWorkerRes()
    encryptionProcessor.do_SplitFile()
    # encryptionProcessor.do_CalculateJobAllocation()
    encryptionProcessor.do_Encrypt()
    encryptionProcessor.do_Decrypt()
    encryptionProcessor.do_MergeFile()
    print('---- System Ending ----')