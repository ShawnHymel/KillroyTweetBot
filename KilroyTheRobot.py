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
#   !fwd - Kilroy moves forward about 15 cm (6 in.)
#   !bck - Kilroy moves backward about 15 cm (6 in.)
#   !lft - Kilroy moves left about 30 deg.
#   !rgt - Kilroy moves right about 30 deg.
#   !pic - Kilroy will count down, snap a picture, and post it to Twitter
#
# For example, to make Kilroy move 30 cm forward, turn right 30 degrees and take
# a picture, send the Tweet:
#
#   @KilroyTheRobot &fwd &fwd &rgt &pic
#
# When posting the picture to Twitter, Kilroy will attempt to tag the requesting
# user.
#-------------------------------------------------------------------------------

import os
import sys
import time
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
    

#-------------------------------------------------------------------------------
# User parameters
#-------------------------------------------------------------------------------

# Debug level
#   0 - Run normally
#   1 - Error and runtime information printed to console
#   2 - Console output, motor drive off
DEBUG = 2

# Automatically shutdown on low battery?
AUTO_SHUTDOWN = True

# Pin assignments
DIR_PIN = 8
DRIVE_PIN = 5
ADC_PIN = 0

# Battery levels
WARN_LEVEL = 40
SHUTOFF_LEVEL = 30

# LED maps file (for eyes)
LEDMAP_FILE = 'ledmaps.txt'

# Alive number file
ALIVE_NUMBER_FILE = 'alive_number.txt'

# Alive number section and variable
ALIVE_NUMBER_SECTION = 'alive_number_section'
ALIVE_NUMBER = 'alive_number'

# Twitter authentication credentials
TWITTER_AUTH = {    'app_key': 'QP9zzvRZWgjDJkGgK8TZ6g',
                    'app_secret': 'wskPbXryJc1bHbESVmkYrfMHvsCVCty8LiEybvTAw',
                    'oauth_token': '2366092298-Wg9ZNFm16QvTBO7LXCx3wGKknGgZKCoU1GFnyH7',
                    'oauth_token_secret': 'wJgAcl4dYHGnDq8RcuUfV8fHzKLWlJ00XNR87Xg94qUXr' }

# The robot's Twitter handle. With an @ sign.
HANDLE = '@KilroyTheRobot'

# Accepted commands along with their appropriate function call
COMMANDS = {'!fwd':drive_forward, 
            '!bck':drive_backward, 
            '!lft':drive_left, 
            '!rgt':drive_right}

# Drive time (in seconds) for [forward, backward, left, right]
DRIVE_TIME = {'fwd':1, 'bck':1, 'lft':0.5, 'rgt':0.5}

# Tweets
START_TWEET = "I'm Kilroy! Send me a tweet with the commands: !fwd !bck !lft \
            !rgt !pic"
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
    
    #***TODO: BATTERY LEVEL MEASUREMENT
    
    val = 0
    return val

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

# Runs the main Kilroy loop. Waits for incoming Tweets and performs actions.
def run_kilroy():

    # Initialize pygame and camera
    pygame.init()
    pygame.camera.init()
    cam = pygame.camera.Camera('/dev/video1', (640, 480))

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
    
        # Get commands and parse them
        cmd_list = tf.get_commands()
        for cmd in cmd_list:
            if cmd[0] == '@':
                user = cmd
            elif cmd == '!pic':
                cam.start()
                img = cam.get_image()
                cam.stop()
                #pygame.image.save(img, 'image.jpg')
                #time.sleep(1)
                #img = open('image.jpg')
                tf.tweet_image(PIC_TWEET + user, img)
            else:
                COMMANDS[cmd](ds)
                
        # Check battery voltage level
        lvl = get_battery_level(ADC_PIN)
        if DEBUG > 0:
            print 'Battery: ' + str(lvl)
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
