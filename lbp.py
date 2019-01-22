import os
import logging
import sys
import json
import broadlink
import binascii
from time import sleep
from Crypto.Cipher import AES

class littleblackpill:
    def __init__(self):
        # CONFIG INIT: 
        self.config = json.loads(open('config.json').read())
        # END CONFIG INIT

        # BROADLINK INIT: 
        devices = []
        if len(self.config['broadlink']['devices']) > 0: 
            for device_config in self.config['broadlink']['devices']: 
                mac_address = device_config['mac'].replace(':', '').decode('hex')
                _device = broadlink.gendevice(device_config['devtype'], (device_config['host']['ip'], device_config['host']['port']), mac_address)
                devices.append(_device)
        else: 
            devices = broadlink.discover(timeout=self.config['broadlink']['discover_timeout'])
        # END BROADLINK INIT
        self.devices = devices

    def perform_action_on_device(self, device, action, qty): 
        # Get our self.config: 
        self.config = json.loads(open('config.json').read())

        # Convert our input to lower case (to match the self.config file):
        device = device.lower()
        action = action.lower()

        # Safely pull our qty int: 
        try: 
            qty = int(qty)
        except: 
            qty = 1

        # Debug output: 
        print("Triggered.")
        print("Device: " + device)
        print("Action: " + action)
        print("QTY: " + str(qty))
        
        # Pull our mapped device, action:
        device = self.config['device_mapping'][device]
        action = self.config['devices'][device]['action_mapping'][action]
        action_data = self.config['devices'][device]['actions'][action]
        action_data = action_data if isinstance(action_data, list) else [ action_data ]
        # Authenticate to our device: 
        self.devices[0].auth()

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
                AESEncryption = AES.new(str(self.devices[0].key), AES.MODE_CFB, str(self.devices[0].iv))
                encryptedCommand = AESEncryption.encrypt(cmd)
                # Fire the command: 
                self.devices[0].send_data(encryptedCommand)
            sleep(self.config['default_pause'])