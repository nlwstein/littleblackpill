import os
import logging
import sys
import json
import broadlink
import binascii
import base64
from time import sleep
from sqs_listener import SqsListener
from Crypto.Cipher import AES

# LOAD CONFIG: 
config = json.loads(open('config.json').read())
# END LOAD CONFIG

# SQS LOGGING: 
logger = logging.getLogger('sqs_listener')
logger.setLevel(logging.INFO)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)

formatstr = '[%(asctime)s - %(name)s - %(levelname)s]  %(message)s'
formatter = logging.Formatter(formatstr)

sh.setFormatter(formatter)
logger.addHandler(sh)
# END SQS LOGGING

# BROADLINK INIT: 
devices = broadlink.discover(timeout=1)
print devices
print "broadlink init!"

class BroadlinkQueueListener(SqsListener):
    def perform_action_on_device(self, device, action, qty):        
        # Convert our input to lower case (to match the config file):
        device = device.lower()
        action = action.lower()

        # Safely pull our qty int: 
        try: 
            qty = int(qty)
        except: 
            qty = 1

        # Debug output: 
        print "Triggered."
        print "Device: " + device
        print "Action: " + action
        print "QTY: " + str(qty)
        
        # Pull our mapped device, action:
        device = config['device_mapping'][device]
        action = config['devices'][device]['action_mapping'][action]
        action_data = config['devices'][device]['actions'][action]
        action_data = action_data if isinstance(action_data, list) else [ action_data ]
        # Authenticate to our device: 
        devices[0].auth()

        # Run the command {qty} times: 
        for i in range(qty): 
            # Re-encrypt the command with the current IV and Key: 
            for cmd in action_data: 
                # HANDLE CUSTOM CASES: 
                if "$PAUSE$" in cmd:
                    seconds = int(cmd.split("$PAUSE$",1)[1])
                    sleep(seconds)
                    continue 
                # END CUSTOM CASES: 
                cmd = binascii.unhexlify(cmd)
                AESEncryption = AES.new(str(devices[0].key), AES.MODE_CFB, str(devices[0].iv))
                encryptedCommand = AESEncryption.encrypt(cmd)
                # Fire the command: 
                devices[0].send_data(encryptedCommand)
            sleep(config['default_pause'])

    def handle_message(self, body, attributes, messages_attributes):
        parameters = body['queryResult']['parameters']
        print parameters['device']
        try: 
            self.perform_action_on_device(parameters['device'], parameters['action'], parameters['qty'])
        except Exception, e:
            print "Something went wrong :( Device: " + parameters['device'] + " Action: " + parameters['action'] + " Message: " + str(e)


listener = BroadlinkQueueListener(config['sqs']['queue'], region_name='us-east-1', wait_time=20, interval=0)
listener.listen()