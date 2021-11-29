#
# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# These materials are licensed under the Amazon Software License in connection with the Alexa Gadgets Program.
# The Agreement is available at https://aws.amazon.com/asl/.
# See the Agreement for the specific terms and conditions of the Agreement.
# Capitalized terms not defined in this file have the meanings given to them in the Agreement.
#

import boto3
import os
import yaml
from pathlib import Path
import board
import neopixel
import logging
import traceback
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartMirrorConfig:
    def __init__(self, parameters):
        self.parameters = parameters
        self.readParameters()
        

    def readParameters(self):
        
        #LedPin
        value = self.getParameterValue('/led/gpio')
        if(value == None):
            value = 21

        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        pin = {
            10: board.D10,
            12: board.D12,
            18: board.D18,
            21: board.D21
        }
        self.LedPin = pin.get(value, board.D21)
        self.LedPinInt = value

        value = self.getParameterValue('/led/count')
        if(value == None):
            value = "60"
        self.LedCount = int(value)

        value = self.getParameterValue('/led/type')
        if(value == None):
            value = "GRBW"
        self.LedType = value

        value = self.getParameterValue('/alexagadget/amazon_id')
        if(value == None):
            value = "XXX"
        self.AlexaGadgetAmazonId = value

        value = self.getParameterValue('/alexagadget/alexa_gadget_secret')
        if(value == None):
            value = "XXX"
        self.AlexaGadgetSecret = value       



    def getParameterValue(self, key):
        for parameter in self.parameters['Parameters']:
            if parameter['Name'] == key:
                return parameter['Value']
        return None

def fetch_and_store_parameters():
    try:
        print('getting parameters')
        hostname=os.uname()[1]
        region=os.getenv('AWS_REGION', 'eu-west-1')
        print('The region we are using is ' + region)

        #read parameters from parameter store
        ssm = boto3.client('ssm',region_name=region)
        parameterPath=f'/smart-mirror/device/{hostname}'
        response = ssm.get_parameters_by_path(Path=parameterPath, Recursive=True, WithDecryption=False)

        # transform and dump yaml file to /home/smart-mirror/conf.yml
        parameters = []
        for parameter in response['Parameters']:
            parameters.append({'Name': parameter['Name'].replace(parameterPath,''), 'Value': parameter['Value']})
            
        config=yaml.dump({'Description': 'Smart Mirror Parameters', 'Parameters': parameters})

        Path("/home/smart-mirror").mkdir(parents=True, exist_ok=True)
        text_file = open('/home/smart-mirror/conf.yml', 'wt')
        text_file.write(config)
        text_file.close()
    except Exception as e:
        logger.info(f'Error in while fetching parameters - Using old parameters if possible: {e}')
        logger.error(f'Stack: {traceback.format_exc()}')


def get_parameters():
    text_file = open('/home/smart-mirror/conf.yml', 'r')
    return yaml.load(text_file)
