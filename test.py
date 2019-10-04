# import subprocess
#
# shl = subprocess.Popen("du -h /nfs-dir/raw-file/16kb-file.txt", shell = True, stdout = subprocess.PIPE)
# stdout = shl.communicate()
# pos = stdout[0].find('\t')
# fileSize = stdout[0][0:pos]
# print fileSize
# satuan = fileSize[-1]
# print satuan
# # print fileSize[0:-1]
#
# if fileSize[-1] is 'K':
#     print 'Kilobyte'
#     realFileSize = int(fileSize[0:-1]) * 1024
# elif fileSize[-1] is 'M':
#     print 'Megabyte'
#     realFileSize = int(fileSize[0:-1]) * 1024 * 1024
# elif fileSize[-1] is 'G':
#     print 'Gigabyte'
#     realFileSize = int(fileSize[0:-1]) * 1024 * 1024 * 1024
# else:
#     print 'Byte'
#     realFileSize = int(fileSize[0:-1])
#
# print realFileSize
#
# shl = subprocess.Popen("split -b 512 /nfs-dir/raw-file/16kb-file.txt /nfs-dir/raw-file/16kb-file.txt.", shell=True, stdout=subprocess.PIPE)
# stdout = shl.communicate()
# print stdout
# Python Program to Get IP Address
# import socket
# hostname = socket.gethostname()
# IPAddr = socket.gethostbyname(hostname)
# print("Your Computer Name is:" + hostname)
# print("Your Computer IP Address is:" + IPAddr)

# numPieces = 32
# jobToAllocate = 12
# workerNum = 1
#

# tes = 'a'
#
# for x in range(5):
#     tes = chr(ord(tes)+1)
#     print tes

# print round(20/26)

# startPart = 20
# jobLength = 12
# keyFile = 'pub16kb-file.txt.pem'
# fileName = '16kb-file.txt'
#
# partDigit = int(round(startPart / 26))
# partDigit += 1
#
# initChar = 'a'
#
# for x in range(21,21+12):
#     print x

# for digit in range(partDigit):
#     for digit in range(26):
#         fileToEncrypt = fileName + "." + initChar
#         print fileToEncrypt
#         print initChar
#         chr(ord(initChar) + 1)
#         print initChar

a = ['192.168.60.181', '192.168.60.182', '192.168.60.183', '192.168.60.184', '192.168.60.185']
print "aku "+str(a)