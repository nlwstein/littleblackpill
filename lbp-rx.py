import os
import logging
import sys
import json
from lbp import littleblackpill
from sqs_listener import SqsListener

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

class BroadlinkQueueListener(SqsListener):
    def __init__(self):
        self.lbp = littleblackpill()

    def handle_message(self, body, attributes, messages_attributes):
        parameters = body['queryResult']['parameters']
        print parameters['device']
        try: 
            lbp.perform_action_on_device(parameters['device'], parameters['action'], parameters['qty'])
        except Exception, e:
            print "Something went wrong :( Device: " + parameters['device'] + " Action: " + parameters['action'] + " Message: " + str(e)
            tb = traceback.format_exc()
            print tb


listener = BroadlinkQueueListener(config['sqs']['queue'], region_name=config['sqs']['region_name'], wait_time=20, interval=0)
listener.listen()