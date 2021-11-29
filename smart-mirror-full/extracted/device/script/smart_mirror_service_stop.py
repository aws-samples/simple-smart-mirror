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

print(f'*************stopping smart-mirror*****************')

parameters = get_parameters()
config =  SmartMirrorConfig(parameters)
smart_mirror = SmartMirror(config)
smart_mirror.reset()