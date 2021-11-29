#
# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# These materials are licensed under the Amazon Software License in connection with the Alexa Gadgets Program.
# The Agreement is available at https://aws.amazon.com/asl/.
# See the Agreement for the specific terms and conditions of the Agreement.
# Capitalized terms not defined in this file have the meanings given to them in the Agreement.
#

import json
import logging
import sys
import fileinput
import os
from os import path
from smart_mirror import SmartMirror
from parameter_store_helper import fetch_and_store_parameters, get_parameters, SmartMirrorConfig

print(f'*************starting smart-mirror*****************')
fetch_and_store_parameters()

parameters = get_parameters()
config =  SmartMirrorConfig(parameters)
smart_mirror = SmartMirror(config)
smart_mirror.reset()
smart_mirror.breathe()
smart_mirror.intro()
smart_mirror.reset()


device_type = config.AlexaGadgetAmazonId
device_type_secret = config.AlexaGadgetSecret
for pkg_path, pkg_name, file_name_list in os.walk("/home/smart-mirror/script"):
    for file_name in file_name_list:
        if file_name.endswith(".ini"):
            for line in fileinput.input(path.join(pkg_path, file_name), inplace=True):
                if "amazonId" in line:
                    print('amazonId = {}'.format(device_type))
                elif "alexaGadgetSecret" in line:
                    print('alexaGadgetSecret = {}'.format(device_type_secret))
                else:
                    print('{}'.format(line), end='')

defaultScript = '/agt_smart_mirror.py'
defaultPath='/home/smart-mirror/script'

print(f'starting {defaultPath}{defaultScript}')

exec(open(f'{defaultPath}{defaultScript}').read())
