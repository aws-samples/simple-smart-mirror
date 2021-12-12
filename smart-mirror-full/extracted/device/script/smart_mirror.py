#
# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# These materials are licensed under the Amazon Software License in connection with the Alexa Gadgets Program.
# The Agreement is available at https://aws.amazon.com/asl/.
# See the Agreement for the specific terms and conditions of the Agreement.
# Capitalized terms not defined in this file have the meanings given to them in the Agreement.
#

import time
import board
import neopixel
import webcolors

from parameter_store_helper import SmartMirrorConfig
from datetime import datetime

class SmartMirror:

    def __init__(self, config):
        self.config = config
        self.pixels = {}
        self.initializePixels()

    def initializePixels(self):
        # Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
        # NeoPixels must be connected to D10, D12, D18 or D21 to work.
        pixel_pin = self.config.LedPin

        # The number of NeoPixels
        num_pixels = self.config.LedCount

        # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
        # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
        ORDER = self.config.LedType

        self.pixels = neopixel.NeoPixel(
            pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER
        )
    
    def updateConfig(self, config):
        self.reset()
        self.config = config
        self.initializePixels()

    def reset(self):
        self.pixels.fill((0,0,0))
        self.pixels.show()

    def showColor(self, color):
        self.pixels.fill(color)
        self.pixels.show()

    def showRange(self, fromPosition, untilPosition, wait, color):
        color = color
        for i in range(0, self.config.LedCount, 1):
            if fromPosition <= i <= untilPosition:
                self.pixels[i] = color
            else:
                self.pixels[i] = (0,0,0)
        self.pixels.show()
        time.sleep(wait) 

    #Turn on specified pixel with specified color
    def showPixel (self, pixel, color):
        self.pixels[pixel] = color
        self.pixels.show()

    def play_intro(self):
        self.reset()
        self.breathe()
        self.intro()
        self.reset()
    
    def intro(self):
        intro_wait = 0.05        
        for i in range(64):
            if (i < 60):
                self.pixels[i] = (0,0,255)
                self.pixels.show()
                time.sleep(intro_wait)
            else:   
                if (i == 60):
                    self.pixels[59] = (0,0,200)
                    self.pixels[58] = (0,0,150)
                    self.pixels[57] = (0,0,100)
                    self.pixels[56] = (0,0,50)
                    self.pixels[55] = (0,0,0)
                if (i == 61):
                    self.pixels[59] = (0,0,150)
                    self.pixels[58] = (0,0,100)
                    self.pixels[57] = (0,0,50)
                    self.pixels[56] = (0,0,0)
                if (i == 62):
                    self.pixels[59] = (0,0,100)
                    self.pixels[58] = (0,0,50)
                    self.pixels[57] = (0,0,0)
                    self.pixels[56] = (0,0,0)
                if (i == 63):
                    self.pixels[59] = (0,0,50)
                    self.pixels[58] = (0,0,0)
                    self.pixels[57] = (0,0,0)
                    self.pixels[56] = (0,0,0)
                self.pixels.show()
                time.sleep(intro_wait)
            if (i == 1):
                self.pixels[i-1] = (0,0,200)

            if (i == 2):
                self.pixels[i-2] = (0,0,150)
                self.pixels[i-1] = (0,0,200)
            
            if (i == 3):
                self.pixels[i-1] = (0,0,200)
                self.pixels[i-2] = (0,0,150)
                self.pixels[i-3] = (0,0,100)
            
            if (i == 4):
                self.pixels[i-1] = (0,0,200)
                self.pixels[i-2] = (0,0,150)
                self.pixels[i-3] = (0,0,100)
                self.pixels[i-4] = (0,0,50)

            if ((i > 4) and (i < 60)):
                self.pixels[i] = (0,0,250)
                self.pixels[i-1] = (0,0,200)
                self.pixels[i-2] = (0,0,150)
                self.pixels[i-3] = (0,0,100)
                self.pixels[i-4] = (0,0,50)
                self.pixels[i-5] = (0,0,0)


    def breathe(self):
        low_power = 30
        high_power = 120
        breathe_wait = 0.015

        print("playing breathe animation")
        for i in range(low_power, high_power, 1):
            self.pixels.fill((i, i, i))
            self.pixels.show()
            time.sleep(breathe_wait)
        for j in range(high_power, low_power, -1):
            self.pixels.fill((j, j, j))
            self.pixels.show()
            time.sleep(breathe_wait)


    def wheel(self, pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos * 3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos * 3)
            g = 0
            b = int(pos * 3)
        else:
            pos -= 170
            r = 0
            g = int(pos * 3)
            b = int(255 - pos * 3)
        return (r, g, b) if self.config.LedType in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

    def blink_color(self, color, times, wait):
        print("Blinking color")
        num_pixels = self.config.LedCount
        chunk = int(num_pixels // 8)
        leftoverpixels = (num_pixels - chunk*8)//2
        blue_start = 0
        white_start = chunk * 3 + leftoverpixels
        white2_start = chunk * 4 + leftoverpixels
        red_start = chunk * 5 + leftoverpixels
        for j in range(times):
            if color == "red":
                for c in range(red_start, red_start + chunk * 3 + leftoverpixels, 1):
                    self.pixels[c] = webcolors.name_to_rgb('red')
            if color == "blue":
                for c in range(blue_start, blue_start + chunk * 3 + leftoverpixels, 1):
                    self.pixels[c] = webcolors.name_to_rgb('blue')
            if color == "white":
                for c in range(white_start, white_start + chunk, 1):
                    self.pixels[c] = (255, 255, 255)
            if color == "white2":
                for c in range(white2_start, white2_start + chunk, 1):
                    self.pixels[c] = (255, 255, 255)
            self.pixels.show()
            time.sleep(wait)
            self.reset()

    def police(self):
        defaultwait = 0.10
        self.reset()
        self.blink_color("red", 4, defaultwait)
        self.blink_color("white", 1, defaultwait * 1.1)
        self.blink_color("blue", 4, defaultwait)
        self.blink_color("white2", 1, defaultwait * 1.1)
        self.blink_color("blue", 2, defaultwait)
        self.blink_color("red", 2, defaultwait)
        self.blink_color("blue", 2, defaultwait)
        self.blink_color("red", 2, defaultwait)
        self.blink_color("white", 1, defaultwait * .1)
        self.blink_color("white2", 1, defaultwait * .1)
        self.blink_color("red", 10, defaultwait)
        self.blink_color("blue", 10, defaultwait)

    def bright_white(self):
        self.reset()
        self.pixels.fill((255, 255, 255))
        self.pixels.show()

    def rainbow_cycle(self, wait):
        num_pixels = self.config.LedCount
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)    

    def clock (self):
        print("Showing Clock")
        self.reset()
        num_pixels = self.config.LedCount
        now = datetime.now()
        hourval = (now.hour % num_pixels % 12) # Adapt to led count, and set 12 hour clock (0-11)
        minutepixel = (now.minute  // (60 // num_pixels) % num_pixels) # Adapt to non 60 led count if needed
        secondpixel = (now.second // (60 // num_pixels) % num_pixels) # Adapt to non 60 led count if needed
        hourpixel = (hourval * 60 + minutepixel) // 12 # Adjusted position relative to minutes   

        ## Define used colors for pixels - using webcolors library for mapping
        hourcolor = webcolors.name_to_rgb('red')
        minutecolor = webcolors.name_to_rgb('blue')
        secondcolor = webcolors.name_to_rgb('green')
        ## Turn on hour - minute - second pixels
        self.showPixel(hourpixel,hourcolor)
        self.showPixel(minutepixel,minutecolor)
        self.showPixel(secondpixel,secondcolor)