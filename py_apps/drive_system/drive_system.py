#-------------------------------------------------------------------------------
# Drive System
#
# Author: Shawn Hymel @ SparkFun Electronics
# Date: April 19, 2014
# License: This code is beerware; if you see me (or any other SparkFun employee)
# at the local, and you've found our code helpful, please buy us a round!
# Distributed as-is; no warranty is given.
#
# Controls Kilroy's drive motor and steering servo.
#-------------------------------------------------------------------------------

import time     
     
#-------------------------------------------------------------------------------
# Class - DriveSystem
#
# Provides an interface to control Kilroy
#-------------------------------------------------------------------------------

class DriveSystem:

    # [Constructor] Setup drive system
    #   Debug level
    #   0 - Run normally
    #   1 - Error and runtime information printed to console
    #   2 - Console output, motor drive off
    def __init__(self, debug=0):
        
        # Declare class members
        self.debug = debug
    
    def drive_forward(self, time_in_sec):
    
        # If debug is on, print to console
        if self.debug > 0:
            print 'Driving forward'
            
        # If motors are not enabled, pretend to drive
        if self.debug > 1:
            time.sleep(time_in_sec)
            print '...done'
        else:
            # Do motor stuff
            pass
            
    def drive_backward(self, time_in_sec):
        
        # If debug is on, print to console
        if self.debug > 0:
            print 'Driving backward'
            
        # If motors are not enabled, pretend to drive
        if self.debug > 1:
            time.sleep(time_in_sec)
            print '...done'
        else:
            # Do motor stuff
            pass
            
    def drive_left(self, time_in_sec):
    
        # If debug is on, print to console
        if self.debug > 0:
            print 'Driving left'
            
        # If motors are not enabled, pretend to drive
        if self.debug > 1:
            time.sleep(time_in_sec)
            print '...done'
        else:
            # Do motor stuff
            pass
            
    def drive_right(self, time_in_sec):
        
        # If debug is on, print to console
        if self.debug > 0:
            print 'Driving right'
            
        # If motors are not enabled, pretend to drive
        if self.debug > 1:
            time.sleep(time_in_sec)
            print '...done'
        else:
            # Do motor stuff
            pass