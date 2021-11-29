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
import threading
import time
from enum import Enum
from datetime import datetime
import dateutil.parser
import traceback
import webcolors

import board
import neopixel

from agt import AlexaGadget
from smart_mirror import SmartMirror
from parameter_store_helper import fetch_and_store_parameters, get_parameters, SmartMirrorConfig

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class Actions(Enum):
    Off = 0
    Rainbow = 1
    Breathe = 2
    ShowColor = 3
    Clock = 4
    Timer = 5
    Police = 6


class SmartMirrorGadget(AlexaGadget):
    """
    An Alexa Gadget for your simple smart mirror.
    """
    def __init__(self):
        super().__init__()

        self.config = self.get_parameters()
        self.smart_mirror = SmartMirror(self.config)

        #This sets what action is starte when the mirror starts
        self.defaultAction = Actions.Clock
        self.currentAction = self.defaultAction
        self.lastAction = self.defaultAction

        # Boolean that tells the loop if it should execute actions or not - default is True which means that the configured default action (self.defaultAction)
        # will be used
        self.keep_cycling = True

        #default options for show color as a reference
        self.showColorOptions = {
            'color': webcolors.name_to_rgb('yellow')
        }

        #default options for timer
        self.showTimerOptions = {
            'startTime': None,
            'endTime': None,
            'color': webcolors.name_to_rgb('red'),
            'timer_token': None
        }

        # Setup a lock to be used for avoiding race conditions
        # during color animation state updates
        self.lock = threading.Lock()
        self.loop_thread = threading.Thread(target=self.loop)
        self.loop_thread.start()

    def get_parameters(self):
        """
        Gets the parameters from parameter store
        """
        try:
            fetch_and_store_parameters()
            parameters = get_parameters()
            return SmartMirrorConfig(parameters)
        except:
            return SmartMirrorConfig({})

    def startAction(self, action):    
        """
        Call this function to start a specific action
        """
        logger.info(f'Starting Action {action}')
        self.lock.acquire()
        self.lastAction = self.currentAction
        self.currentAction = action
        self.keep_cycling = True
        self.lock.release()

    def stopAction(self):
        """
        Call this action to end the current action - turn all LEDs off
        """
        self.lock.acquire()
        self.lastAction = Actions.Off
        self.currentAction = Actions.Off
        self.keep_cycling = False
        self.lock.release()

    def loop(self):
        """
        Main function of this class. This is an endless loop running in a separate thread. It will check what action to run on each iteration.
        """
        while True:
            # Check if anything should be visualized
            if self.keep_cycling:
                logger.info(f'{self.currentAction} is on')
                try:
                    if self.currentAction == Actions.Off:
                        time.sleep(0.1)
                    if self.currentAction == Actions.Rainbow:
                        self.smart_mirror.rainbow_cycle(0.001)
                    if self.currentAction == Actions.Breathe:
                        self.smart_mirror.breathe()
                    if self.currentAction == Actions.Police:
                        self.smart_mirror.police()
                    if self.currentAction == Actions.Clock:
                        self.smart_mirror.clock()
                    if self.currentAction == Actions.ShowColor:
                        self.smart_mirror.showColor(
                            self.showColorOptions['color'])
                    if self.currentAction == Actions.Timer:
                        timerPosition = self.getCurrentTimerPosition()
                        if(timerPosition != 0):
                            self.smart_mirror.showRange(0, timerPosition, 0.1, self.showTimerOptions['color'])
                        else:
                            self.smart_mirror.showColor(self.showTimerOptions['color'])
                except Exception as e:
                    logger.info(f'Error in loop: {e}')
                    logger.error(f'Stack: {traceback.format_exc()}')
                    time.sleep(0.1)
            else:
                logger.info('Nothing is on')
                self.smart_mirror.reset()
                time.sleep(0.1)

    def on_alexa_gadget_statelistener_stateupdate(self, directive):
        """
        This will trigger when your connected Alexa device changes state. Here we listening for your Alexa to react to you saying "Alexa..." or "Echo..."
        """
        for state in directive.payload.states:
            if state.name == 'wakeword':
                if state.value == 'active':
                    logger.info('Wake word active')
                    self.showColorOptions['color'] = webcolors.name_to_rgb('yellow')
                    self.startAction(Actions.ShowColor)
                elif state.value == 'cleared':
                    logger.info('Wake word cleared')
                    self.startAction(self.lastAction)

    def on_alerts_setalert(self, directive):
        """
        Handles setting of alerts on your connected Alexa device e.g. "Alexa set timer for 60 seconds"
        """
        if directive.payload.type != 'TIMER':
            logger.info(
                "Received SetAlert directive but type != TIMER. Ignorning")
            return

        endTime = dateutil.parser.parse(directive.payload.scheduledTime).timestamp()
        now = time.time()

        if endTime <= 0:
            logger.info(
                "Received SetAlert directive but scheduledTime has already passed. Ignoring")
            return

        if self.showTimerOptions['timer_token'] == directive.payload.token:
            logger.info(
                "Received SetAlert directive to update to currently running timer. Adjusting")
            self.showTimerOptions['endTime'] = endTime
            return

        if self.currentAction == Actions.Timer:
            logger.info(
                "Received SetAlert directive but another timer is already running. Ignoring")
            return

        logger.info("Received SetAlert directive. Starting a timer. " +
                    str(int(endTime - now)) + " seconds left..")
        self.showTimerOptions['endTime'] = endTime
        self.showTimerOptions['startTime'] = now
        self.showTimerOptions['timer_token'] = directive.payload.token
        self.showTimerOptions['color'] = webcolors.name_to_rgb('red')

        self.startAction(Actions.Timer)

    def on_alerts_deletealert(self, directive):
        """
        Handles deletion of alert - reverts back to default action
        """
        self.startAction(self.defaultAction)

    def getCurrentTimerPosition(self):
        """
        Figure out how many LEDs should be turned on. If the timer is up all 60 LEDs shoul be lit.
        """
        start_time = self.showTimerOptions['startTime']
        logger.info("start_time " + str(start_time) + " in timer")  # Log stuff

        end_time = self.showTimerOptions['endTime']
        logger.info("end_time " + str(end_time) + " in timer")  # Log stuff

        current_time = time.time()
        logger.info("current_time " + str(current_time) +
                    " in timer")  # Log stuff

        timer_total = int(end_time - start_time)
        logger.info("timer_total " + str(timer_total) +
                    " in timer")  # Log stuff

        timer_left = int(max(0, end_time - current_time))
        logger.info("timer_left " + str(timer_left) + " in timer")  # Log stuff

        if timer_left > 0:
            nextPosition = int((timer_total - timer_left)/timer_total * self.config.LedCount)
            logger.info("Next position " + str(nextPosition) +
                        " in timer")  # Log stuff
            logger.info("LedCount/Modulo:" +
                        str(self.config.LedCount))  # Log stuff
            time.sleep(1)
            return nextPosition  # Light up the leds
        else:
            return 0

    # this matches the namespace that the skill adds in the payload (see lambda_function.py): (namespace='Custom.SmartMirror', name='Rainbow'),
    def on_custom_smartmirror_rainbow(self, directive):
        """
        Handles Custom.SmartMirror.Rainbow directive
        """

        logger.info('show rainbow directive called')

        self.startAction(Actions.Rainbow)

    # this matches the namespace that the skill adds in the payload (see lambda_function.py): (namespace='Custom.SmartMirror', name='Color'),
    def on_custom_smartmirror_color(self, directive):
        """
        Handles Custom.SmartMirror.Color directive
        """
        payload = json.loads(directive.payload.decode("utf-8"))
        color = payload['color'].lower() #this is the color name coming in from Alexa
        rgb = webcolors.name_to_rgb(color)
        logger.info(f'show color directive called with color {color} => {rgb}')

        self.showColorOptions['color'] = rgb        
        self.startAction(Actions.ShowColor)

    # this matches the namespace that the skill adds in the payload (see lambda_function.py): (namespace='Custom.SmartMirror', name='Clock'),
    def on_custom_smartmirror_clock(self, directive):
        """
        Handles Custom.SmartMirror.Clock directive
        """

        logger.info('show clock directive called')

        self.startAction(Actions.Clock)

    def on_custom_smartmirror_police(self, directive):
        """
        Handles Custom.SmartMirror.Police directive
        """
        logger.info('Blink like the Police')
        self.startAction(Actions.Police)

    def on_custom_smartmirror_stopled(self, directive):
        """
        Handles Custom.ColorCyclerGadget.StopLED directive sent from skill
        by stopping the LED animations
        """
        logger.info('StopLED directive received: Turning off LED')

        self.stopAction()

    def reset(self):
        """
        Turn off all LEDs by calling the reset function
        """
        try:
            self.smart_mirror.reset()
        except:
            print(f'failed to reset')


if __name__ == '__main__':
    gadget = SmartMirrorGadget()
    try:
        gadget.main()
    finally:
        gadget.reset()
