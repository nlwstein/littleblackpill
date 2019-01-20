import os
import logging
import sys
import json
import broadlink
import base64
import binascii
import pickle
from time import sleep
from sqs_listener import SqsListener
from Crypto.Cipher import AES

devices = broadlink.discover(timeout=1)
print devices
device = devices[0]
device.auth()
device.enter_learning()
print "entering learning..."
sleep(5)
print "dumping decrypted config value..."
LearnedCommand = device.check_data()
AESEncryption = AES.new(str(device.key), AES.MODE_CFB, str(device.iv))
decryptedCommand = AESEncryption.decrypt(LearnedCommand)
configValue = binascii.hexlify(decryptedCommand)
print "config value: " + configValue