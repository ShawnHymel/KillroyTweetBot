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

#-------------------------------------------------------------------------------
# Robot functions
#-------------------------------------------------------------------------------

# Drive Kilroy forward
def drive_forward(ds, user):
    ds.drive_forward(DRIVE_TIME['fwd'])
    
# Drive Kilroy backward
def drive_backward(ds, user):
    ds.drive_backward(DRIVE_TIME['bck'])
    
# Drive Kilroy left
def drive_left(ds, user):
    ds.drive_left(DRIVE_TIME['lft'])
    
# Drive Kilroy right
def drive_right(ds, user):
    ds.drive_right(DRIVE_TIME['rgt'])
    
# Take a picture and post to Twitter
def take_picture(ds, user):
    print 'Taking picture, ' + user

#-------------------------------------------------------------------------------
# User parameters
#-------------------------------------------------------------------------------

# Debug level
#   0 - Run normally
#   1 - Error and runtime information printed to console
#   2 - Console output, motor drive off
DEBUG = 2

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
            '!rgt':drive_right, 
            '!pic':take_picture}

# Drive time (in seconds) for [forward, backward, left, right]
DRIVE_TIME = {'fwd':1, 'bck':1, 'lft':0.5, 'rgt':0.5}
                    
#-------------------------------------------------------------------------------
# Import custom modules
#-------------------------------------------------------------------------------

# Add motor_driver module to path
path = os.path.join(os.path.dirname(__file__), 'py_apps/drive_system')
sys.path.append(path)

# Add tweet_feed module to path
path = os.path.join(os.path.dirname(__file__), 'py_apps/tweet_feed')
sys.path.append(path)

import drive_system
import tweet_feed

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Global Variables
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

# Runs the main Kilroy loop. Waits for incoming Tweets and performs actions.
def run_kilroy():

    # Initialize user
    user = None

    # Create a TweetFeed object
    tf = tweet_feed.TweetFeed(TWITTER_AUTH, DEBUG)
    
    # Create a DriveSystem object
    ds = drive_system.DriveSystem(DEBUG)
    
    # Get start time
    start_time = time.time()
    
    # Start Twitter API streamer to look for Tweets at Kilroy
    tf.start_streamer(HANDLE, COMMANDS)
    
    #***TEST***
    print 'Here we go! Waiting for ' + HANDLE
    while ((time.time() - start_time) < 30):
        cmd_list = tf.get_commands()
        for cmd in cmd_list:
            if cmd[0] == '@':
                user = cmd
            else:
                COMMANDS[cmd](ds, user)
        time.sleep(0.1)
    
    print 'I\'m tired. I think I\'ll take a nap.'
    tf.stop_streamer()

    return

# Run main
if __name__ == "__main__":
    run_kilroy()
