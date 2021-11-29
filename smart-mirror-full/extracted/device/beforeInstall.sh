#
# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# These materials are licensed under the Amazon Software License in connection with the Alexa Gadgets Program.
# The Agreement is available at https://aws.amazon.com/asl/.
# See the Agreement for the specific terms and conditions of the Agreement.
# Capitalized terms not defined in this file have the meanings given to them in the Agreement.
#

#!/bin/bash

echo "before install"

{ # try
    echo "ending process if already running"
    kill $(ps aux | grep '[p]ython3.*rainbow.py' | awk '{print $2}')
    echo "ended application"

} || { # catch
    echo "not running"
}

serviceStatus=$(systemctl is-active smart-mirror)


if [ $serviceStatus == "active" ]
then
	systemctl stop smart-mirror
fi


#Removing service if already installed
echo "Removing smart-mirror.service"
rm -f /etc/systemd/system/smart-mirror.service
echo "Removed smart-mirror.service"

echo "installing"

touch /tmp/installing.log


echo "installing dependencies"

apt-get update -y
apt-get install -y python3-pip git

pip3 install --no-cache-dir rpi_ws281x adafruit-circuitpython-neopixel boto3 pyyaml webcolors
python3 -m pip install adafruit-blinka

