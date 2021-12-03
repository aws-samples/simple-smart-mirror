# Smart Mirror Pre-requisites
-----------------------

Table of contents:
<!-- AUTO-GENERATED-CONTENT:START (TOC) -->
- [Amazon Alexa Developer Account](#amazon-alexa-developer-account)
- [AWS Account](#aws-account)
- [AWS costs from this project](#aws-costs-from-this-project)
- [Hardware shopping list for Smart Mirror](#hardware-shopping-list-for-smart-mirror)
<!-- AUTO-GENERATED-CONTENT:END -->

## Amazon Alexa Developer Account

Create or have access to [Amazon Developer Services](https://developer.amazon.com/) account - sign-up is free - if you do not have account then create one

> **_NOTE:_** This account owns your Alexa skill for Smart Mirror. Make sure the account you are using is the same account you use in your Alexa device (Phone / Echo) and connect this with AWS CodeStar

## AWS Account

If you do not have existing AWS account please see instructions how to create one.

Please see [Create and activate AWS Account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/)

> **_NOTE:_** We use AWS region Ireland (eu-west-1) throughout examples - other regions should work as well.

## AWS costs from this project

This solution will incur cost based on your usage.
- Used services are [AWS Free Tier eligible](https://aws.amazon.com/free/)

Free tier covers:
* EC2 for Cloud9 (running only when IDE is used - by default it shuts down after 30 minutes)
* Persistent storage (S3 Artifacts + EBS for Cloud9)
* Data Transfer out is free up to 100GB
* One active AWS CodePipeline

Additional costs:
There is cost per on-premise AWS CodeDeploy deployment as per https://aws.amazon.com/codedeploy/pricing/ 

Estimation of cost outside of Free Tier is less than 1$ per month - depending on number of deployments you make.

## Hardware shopping list for Smart Mirror

Smart Mirror HW components shopping list

Shopping List - with Amazon.com examples - please use shop near you:
* Mirror - best is a round mirror with diameter as close to 31.83cm / 12.53in as possible 
* LED strip - 1 meter programmable (preferable adafruit neopixel): 
    * [Amazon.com](https://www.amazon.com/Adafruit-Indust-Digital-Weatherproof-LED-1m/dp/B01KHWGVJ4/ref=sr_1_7?keywords=neopixel+1m+60&qid=1637236557&sr=8-7)
* Raspberry Pi 4 model B 8 GB: (4GB model or even Raspberry Pi 3 should also work, but see GPIO ports is using PI 3)
    * [Amazon.com](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TC2BK1X/)
* Raspberry Pi Power Supply (USB C, 5V 3+A) - please use good quality power supply to have enough power for 60 LEDs
    * [Amazon.com](https://www.amazon.com/Raspberry-Power-Supply-USB-C-Listed/dp/B07Z8P61DQ/)
* SD Card: 
    * [Amazon.com](https://www.amazon.com/16GB-Raspberry-Preloaded-Noobs-Card/dp/B07GTDD1L5/)
* Electronics:
    * Capacitor 1000 uF (set)
        * [Amazon.com](https://www.amazon.com/OCR-Electrolytic-Capacitor-Assortment-0-1uF%EF%BC%8D1000uF/dp/B01MSQOX0Q/)
    * Resistor 470 Ohm (set)
        * [Amazon.com](https://www.amazon.com/Elegoo-Values-Resistor-Assortment-Compliant/dp/B072BL2VX1/)
    * Breadboard
        * [Amazon.com](https://www.amazon.com/Breadboards-Solderless-Breadboard-Distribution-Connecting/dp/B07DL13RZH)
    * Some Cables for the Breadboard e.g. Female/Male and Male/Male
        * [Amazon.com](https://www.amazon.com/Elegoo-EL-CP-004-Multicolored-Breadboard-arduino/dp/B01EV70C78)
    * Some Cable to connect Breadboard/Raspberry Pi with LED strip
        * [Amazon.com](https://www.amazon.com/BTF-LIGHTING-Connectors-WS2812B-WS2811-WS2812/dp/B01DC0KIT2)
* Alexa Echo - any echo (e.g echo dot 3 with bluetooth will work)
    * [Amazon.com](https://www.amazon.com/s?k=echo+dot+bluetooth)




