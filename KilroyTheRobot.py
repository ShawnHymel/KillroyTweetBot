#-------------------------------------------------------------------------------
# KillroyTheRobot
#
# Author: Shawn Hymel @ SparkFun Electronics
# Date: April 14, 2014
# License: This code is beerware; if you see me (or any other SparkFun employee)
# at the local, and you've found our code helpful, please buy us a round!
# Distributed as-is; no warranty is given.
#
# Listens for Tweets sent to @KillroyTheRobot and parses the Tweet for commands.
# Special '&' tagged commands in the Tweet will cause Kilroy to perform certain
# actions. The command Tweet must be in the form:
#
#   @KilroyTheRobot [commands separated by spaces]
#
# The accepted commands are:
#
#   forward - Kilroy moves forward about 15 cm (6 in.)
#   back - Kilroy moves backward about 15 cm (6 in.)
#   left - Kilroy moves left about 30 deg.
#   right - Kilroy moves right about 30 deg.
#   pic - Kilroy will count down, snap a picture, and post it to Twitter
#
# For example, to make Kilroy move 30 cm forward, turn right 30 degrees and take
# a picture, send the Tweet:
#
#   @KilroyTheRobot &fwd &fwd &rgt &pic
#
# When posting the picture to Twitter, Kilroy will attempt to tag the requesting
# user.
#
# IMPORTANT: USB needs resetting! Find camera and reset:
#
#   $ lsusb
#   $ sudo ./usbreset /dev/bus/usb/002/003
#
# Source: http://askubuntu.com/questions/645/how-do-you-reset-a-usb-device-from-the-command-line
#
# TODO:
#  - Fix keypress exit
#  - Fix USB reset issues
#-------------------------------------------------------------------------------

import os
import sys
import termios
import time
import tty
import pygame
import pygame.camera

#-------------------------------------------------------------------------------
# Drive functions (callbacks from command parser)
#-------------------------------------------------------------------------------

# Drive Kilroy forward
def drive_forward(ds):
    ds.drive_forward(DRIVE_TIME['fwd'])
    
# Drive Kilroy backward
def drive_backward(ds):
    ds.drive_backward(DRIVE_TIME['bck'])
    
# Drive Kilroy left
def drive_left(ds):
    ds.drive_left(DRIVE_TIME['lft'])
    
# Drive Kilroy right
def drive_right(ds):
    ds.drive_right(DRIVE_TIME['rgt'])

# Take picture (placeholder)
def take_picture(ds):
    return    

#-------------------------------------------------------------------------------
# User parameters
#-------------------------------------------------------------------------------

# Debug level
#   0 - Run normally
#   1 - Error and runtime information printed to console
#   2 - Console output, motor drive off
DEBUG = 1

# Automatically shutdown on low battery?
AUTO_SHUTDOWN = True

# Camera USB location
USB_CAM = '/dev/bus/usb/003/004'

# Pin assignments
DIR_PIN = 8
DRIVE_PIN = 5
ADC_PIN = 0

# Battery levels
WARN_LEVEL = 51
SHUTOFF_LEVEL = 49

# Camera file
CAM_FILE = '/dev/video0'

# LED maps file (for eyes)
LEDMAP_FILE = 'ledmaps.txt'

# Alive number file
ALIVE_NUMBER_FILE = 'alive_number.txt'

# Alive number section and variable
ALIVE_NUMBER_SECTION = 'alive_number_section'
ALIVE_NUMBER = 'alive_number'

# ADC file
ADC_FILE = '/proc/adc0'

# Twitter authentication credentials
TWITTER_AUTH = {    'app_key': 'QP9zzvRZWgjDJkGgK8TZ6g',
                    'app_secret': 'wskPbXryJc1bHbESVmkYrfMHvsCVCty8LiEybvTAw',
                    'oauth_token': '2366092298-Wg9ZNFm16QvTBO7LXCx3wGKknGgZKCoU1GFnyH7',
                    'oauth_token_secret': 'wJgAcl4dYHGnDq8RcuUfV8fHzKLWlJ00XNR87Xg94qUXr' }

# The robot's Twitter handle. With an @ sign.
HANDLE = '@KilroyTheRobot'

# Accepted commands along with their appropriate function call
COMMANDS = {'forward':drive_forward, 
            'back':drive_backward, 
            'left':drive_left, 
            'right':drive_right,
            'pic':take_picture}

# Drive time (in seconds) for [forward, backward, left, right]
DRIVE_TIME = {'fwd':1, 'bck':1, 'lft':0.5, 'rgt':0.5}

# Tweets
START_TWEET = "I'm Kilroy! Send me a tweet with the commands: forward back left right pic"
END_TWEET = "I'm tired. I think I'll take a nap."
PIC_TWEET = "Domo arigato, "
LOW_BATT_TWEET = "Help me, @ShawnHymel, you're my only hope."
                    
#-------------------------------------------------------------------------------
# Import custom modules
#-------------------------------------------------------------------------------

# Add motor_driver module to path
path = os.path.join(os.path.dirname(__file__), 'py_apps/drive_system')
sys.path.append(path)

# Add tweet_feed module to path
path = os.path.join(os.path.dirname(__file__), 'py_apps/tweet_feed')
sys.path.append(path)

# Add led_driver module to path
path = os.path.join(os.path.dirname(__file__), 'py_apps/led_driver')
sys.path.append(path)

import drive_system
import tweet_feed
import led_driver
import ConfigParser

#-------------------------------------------------------------------------------
# Global Variables
#-------------------------------------------------------------------------------

g_alive_number = None

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

def increment_alive_number():
    global g_alive_number
    
    # Open text file
    config = ConfigParser.RawConfigParser()
    config.read(ALIVE_NUMBER_FILE)
    g_alive_number = int(config.get(ALIVE_NUMBER_SECTION, ALIVE_NUMBER))
    
    # Increment alive number in param file for next time
    config.set(ALIVE_NUMBER_SECTION, ALIVE_NUMBER, str(g_alive_number + 1))
    param_file = open(ALIVE_NUMBER_FILE, 'w')
    config.write(param_file)
    param_file.close()
    del config

# Returns the ADC pin value
def get_battery_level(pin):
    
    # Open ADC file and read value
    fd = open(ADC_FILE, 'r')
    fd.seek(0)
    val = fd.read(16)
    
    return val

# Get a key that has been pressed (from Clark on raspberrypi.org/forums)
def get_key():
   fd = sys.stdin.fileno()
   old = termios.tcgetattr(fd)
   new = termios.tcgetattr(fd)
   new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
   new[6][termios.VMIN] = 1
   new[6][termios.VTIME] = 0
   termios.tcsetattr(fd, termios.TCSANOW, new)
   key = None
   try:
      key = os.read(fd, 3)
   finally:
      termios.tcsetattr(fd, termios.TCSAFLUSH, old)
   return key

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

# Runs the main Kilroy loop. Waits for incoming Tweets and performs actions.
def run_kilroy():

    # Initialize pygame and camera
    pygame.init()
    pygame.camera.init()
    cam = pygame.camera.Camera(CAM_FILE, (640, 480))

    # Initialize user
    user = ''
    
    # Create an LEDDRiver object and draw dead eyes first
    ld = led_driver.LEDDriver(LEDMAP_FILE, DEBUG)
    ld.draw_eyes('dead left', 'dead right')

    # Create a TweetFeed object
    tf = tweet_feed.TweetFeed(TWITTER_AUTH, DEBUG)
    
    # Create a DriveSystem object
    ds = drive_system.DriveSystem(DIR_PIN, DRIVE_PIN, DEBUG)
    
    # Get start time
    start_time = time.time()
    
    # Increment alive counter
    increment_alive_number()

    # Send hello tweet
    tf.tweet(str(g_alive_number) + ': ' + START_TWEET)
    
    # Start Twitter API streamer to look for Tweets at Kilroy
    tf.start_streamer(HANDLE, COMMANDS)
    
    # Main loop
    warning_sent = False
    ld.draw_eyes('open left', 'open right')
    if DEBUG > 0:
        print 'Here we go! Waiting for ' + HANDLE
    while True:
        
        # Look for keypresses and end game on quit
        #if str(get_key()) == 'q':
        #    break

        # Get commands and parse them
        cmd_list = tf.get_commands()
        for cmd in cmd_list:
            if cmd[0] == '@':
                user = cmd
            elif cmd == 'pic':
                #***Cludgey USB restart
                os.system('sudo ./usbreset ' + USB_CAM)
                if DEBUG > 0:
                    print 'Taking picture'
                pygame.camera.init()
                cam = pygame.camera.Camera(CAM_FILE, (640, 480))
                cam.start()
                img = cam.get_image()
                cam.stop()
                pygame.image.save(img, 'image.jpg')
                time.sleep(1)
                img = open('image.jpg')
                tf.tweet_image(PIC_TWEET + user, img)
            else:
                COMMANDS[cmd](ds)
                
        # Check battery voltage level
        lvl = get_battery_level(ADC_PIN)
        lvl = int(lvl[5:])
        if DEBUG > 0:
            #print 'Battery: ' + str(lvl)
            pass
        if (lvl > SHUTOFF_LEVEL) and (lvl <= WARN_LEVEL) and not warning_sent:
            tf.tweet(str(g_alive_number) + ': ' + LOW_BATT_TWEET)
            ld.draw_eyes('sleepy left', 'sleepy right')
            warning_sent = True
        elif (lvl <= SHUTOFF_LEVEL):
            break
        
        # Sleep
        time.sleep(0.1)
    
    # Send goodbye tweet and shut down
    if DEBUG > 0:
        print 'I\'m tired. I think I\'ll take a nap.'
    tf.tweet(str(g_alive_number) + ': ' + END_TWEET)
    tf.stop_streamer()
    
    # If auto-shutdown is enabled, shutdown Linux
    if AUTO_SHUTDOWN:
        #***TODO: SHUTDOWN LINUX
        pass

    return

# Run main
if __name__ == "__main__":
    run_kilroy()
