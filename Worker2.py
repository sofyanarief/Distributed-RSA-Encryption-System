from SimpleXMLRPCServer import SimpleXMLRPCServer
import logging
import psutil
import re
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import zlib
import base64

logging.basicConfig(level=logging.DEBUG)

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

server = SimpleXMLRPCServer((IPAddr, 8000), logRequests=True, allow_none=True);
server.register_multicall_functions()

filePath = '/nfs-dir/'
rawFilePath = 'raw-file/'
keyFilePath = 'key-file/'
encryptedFilePath = 'enc-file/'
decryptedFilePath = 'dec-file/'


def get_CPU_Load():
    cpuLoad = repr(psutil.cpu_percent(interval=1, percpu=False))
    # cpuLoad = '20%'
    logging.debug('CPU Load = %s', cpuLoad)
    return cpuLoad


def get_RAM_Used():
    mem_info = repr(psutil.virtual_memory())
    mem_info_arr = re.split(',', mem_info)
    global used_mem_perc
    used_mem_perc = re.split('=', mem_info_arr[2])
    logging.debug('RAM Used = %s', used_mem_perc[1])
    return used_mem_perc[1]


def get_RAM_Free():
    free_mem_perc = 100 - float(used_mem_perc[1])
    logging.debug('RAM Free = %s', repr(free_mem_perc))
    return repr(free_mem_perc)

# def do_EncryptFile(startPart,jobLength,keyFile,fileName):
#     startPart = 20
#     jobLength = 12
#     keyFile = 'pub16kb-file.txt.pem'
#     fileName = '16kb-file.txt'
#
#     partDigit = round(startPart/26)
#     partDigit += 1
#
#     initChar = 'a'
#
#     for digit in partDigit:
#         for digit in range(26):
#             fileToEncrypt = fileName + "." + initChar
#             print fileToEncrypt

def encrypt_blob(blob, public_key):
    #Import the Public Key and use for encryption using PKCS1_OAEP
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    #compress the data first
    blob = zlib.compress(blob)

    #In determining the chunk size, determine the private key length used in bytes
    #and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
    #in chunks
    chunk_size = 470
    offset = 0
    end_loop = False
    encrypted =  ""

    while not end_loop:
        #The chunk
        chunk = blob[offset:offset + chunk_size]

        #If the data chunk is less then the chunk size, then we need to add
        #padding with " ". This indicates the we reached the end of the file
        #so we end loop here
        if len(chunk) % chunk_size != 0:
            end_loop = True
            chunk += " " * (chunk_size - len(chunk))

        #Append the encrypted chunk to the overall encrypted file
        encrypted += rsa_key.encrypt(chunk)

        #Increase the offset by chunk size
        offset += chunk_size

    #Base 64 encode the encrypted file
    return base64.b64encode(encrypted)

def do_EncryptFile(fileNameToEnc, fileName):
    keyName = 'pub' + fileName + '.pem'
    fd = open(filePath + keyFilePath + keyName, 'rb')
    public_key = fd.read()
    fd.close()

    # Our candidate file to be encrypted
    fd = open(filePath + rawFilePath + fileNameToEnc, 'rb')
    unencrypted_blob = fd.read()
    fd.close()

    encrypted_blob = encrypt_blob(unencrypted_blob, public_key)

    # Write the encrypted contents to a file
    fd = open(filePath + encryptedFilePath + fileNameToEnc, 'wb')
    fd.write(encrypted_blob)
    fd.close()

server.register_function(get_CPU_Load)
server.register_function(get_RAM_Used)
server.register_function(get_RAM_Free)
server.register_function(do_EncryptFile)

try:
    print 'Use Control-C to exit'
    print 'Your Computer IP Address is:' + IPAddr
    server.serve_forever()
except KeyboardInterrupt:
    print 'Exiting'
