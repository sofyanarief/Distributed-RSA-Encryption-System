import threading
import time

from EncryptionProcessor import EncryptionProcessor

if __name__ == '__main__':
    print('---- System Starting ----')
    encryptionProcessor = EncryptionProcessor()
    encryptionProcessor.set_fileName('50mb-file')
    # encryptionProcessor.set_fileName('1mb-file.txt')
    encryptionProcessor.set_keySize(4096)
    encryptionProcessor.do_GenerateKeyForFile()
    # encryptionProcessor.set_workerIP(['192.168.1.31', '192.168.1.32', '192.168.1.33', '192.168.1.34'])
    encryptionProcessor.set_workerIP(['192.168.1.36'])
    encryptionProcessor.get_AllWorkerRes()
    encryptionProcessor.do_SplitFile()
    encryptionProcessor.do_CalculateJobAllocation()
    encryptionProcessor.do_Encrypt()
    encryptionProcessor.do_Decrypt()
    encryptionProcessor.do_MergeFile()
    encryptionProcessor.do_CleaningTempFile()
    print('---- System Ending ----')