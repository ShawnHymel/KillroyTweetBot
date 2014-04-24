#-------------------------------------------------------------------------------
# Drive System
#
# Author: Shawn Hymel @ SparkFun Electronics
# Date: April 22, 2014
# License: This code is beerware; if you see me (or any other SparkFun employee)
# at the local, and you've found our code helpful, please buy us a round!
# Distributed as-is; no warranty is given.
#
# Controls Kilroy's "eyes" (LED matrices). Run "read_sprites.py" first to 
# generate LED maps (saved in ledmaps.txt).
#-------------------------------------------------------------------------------

import os
import spi

#-------------------------------------------------------------------------------
# Class - LEDDriver
#
# Provides an interface to control Kilroy's eyes
#-------------------------------------------------------------------------------

class LEDDriver:

    # [Constructor] Setup drive system
    #   Debug level
    #   0 - Run normally
    #   1 - Error and runtime information printed to console
    #   2 - Console output, no output to SPI
    def __init__(self, ledmap_file, debug=0):
    
        # Set class memebers
        self.debug = debug
    
        # Read in LED maps
        with open(ledmap_file, 'r') as f:
            content = f.read()
        self.led_dict = eval(content)
        
        # Set pin modes
        if debug < 2:
            MODE = 2
            MODE_FILE = '/sys/devices/virtual/misc/gpio/mode/gpio'
            for i in range(10, 14):
                file = MODE_FILE + str(i)
                os.system('echo ' + str(MODE) + ' > ' + file)
            
        # Initialize SPI
        if debug < 2:
            spi.openSPI(speed=100000, mode=0, device='/dev/spidev0.0')
            
        # Clear eyes
        self.clear_eyes()
            
    # Clear LED matrix
    def clear_eyes(self):
        if self.debug > 0:
            print 'Clearing eyes'
        if self.debug < 2:
            data = [0x26]
            spi.transfer(tuple(data))
            data = []
            for i in range(0, 64):
                    data.append(0x00)
            spi.transfer(tuple(data))
            time.sleep(0.01)
            spi.transfer(tuple(data))
            
    # Draw eyes on LED matrices
    def draw_eyes(self, left_eye, right_eye):
        if self.debug > 0:
            print 'Drawing eyes: ' + left_eye + ', ' + right_eye
        if self.debug < 2:
            data = [0x26]
            spi.transfer(tuple(data))
            spi.transfer(tuple(led_dict[right_eye]))
            time.sleep(0.01)
            spi.transfer(tuple(led_dict[left_eye]))
