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
import os
import fcntl
from struct import *  
     
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
    def __init__(self, dir_pin, drive_pin, steer_pin, debug=0):
    
        # Constants
        self.SPEED = 255
        self.FORWARD = 1
        self.BACKWARD = 0
        self.PWM_FREQ = 520
        self.DRIVE_TIME = 1
        self.TURN_TIME = 1
        self.SERVO_LEFT = 0
        self.SERVO_RIGHT = 180
        self.SERVO_CENTER = 90
        
        # Declare class members
        self.debug = debug
        self.dir_pin = dir_pin
        self.drive_pin = drive_pin
        self.steer_pin = steer_pin
        
        # Construct file locations
        self.dir_mode_file = '/sys/devices/virtual/misc/gpio/mode/gpio' + \
                                                            str(self.dir_pin)
        self.dir_file = '/sys/devices/virtual/misc/gpio/pin/gpio' + \
                                                            str(self.dir_pin)
        self.pwm_file = '/dev/pwmtimer'
        self.servo_file = '/dev/ttyUSB0'
        
        # Configure direction pin as output
        if self.debug < 2:
            os.system('echo 1' + ' > ' + self.dir_mode_file)
        
        # Configure PWM
        if self.debug < 2:
            with open(self.pwm_file, 'wb') as f:
                pwm_struct = pack('iiiI', self.steer_pin, 0, 0, PWM_FREQ)
                fcntl.ioctl(f, 0x107, pwm_struct)
                
        # Stop drive motor and set servo to center
        if self.debug < 2:
            self.drive_motor(self.FORWARD, 0)
            self.drive_servo(self.CENTER)
        
    # [Private] Direct motor drive
    def drive_motor(dir, pwm):
    
        # Set direction
        os.system('echo ' + str(dir) + ' > ' + self.drive_dir_file)
        
        # Output PWM to motor
        with open(self.pwm_file, 'wb') as f:
            pwm_struct = pack('ii', self.drive_pin, pwm)
            fcntl.ioctl(f, 0x106, pwm_struct)
            
    # [Private] Direct servo drive (angle is 0 to 180)
    def drive_servo(angle):
    
        # Configure servo
        servo = serial.Serial(self.servo_file, 9600, timeout=10)
        
        # Construct servo angle string
        hex_str = str(hex(angle))
        hex_str = list(hex_str[2:])
        if len(hex_str) < 2:
            hex_str.insert(0, '0')
        hex_str = unicode("".join(hex_str))
        
        # Create bytearray and send to servo controller
        data = bytearray.fromhex(hex_str)
        servo.write(data)
        
        # Close serial file
        servo.close()
        
        return
    
    # [Public] Drive forward for given time
    def drive_forward(self, time_in_sec):
    
        # If debug is on, print to console
        if self.debug > 0:
            print 'Driving forward'
            
        # If motors are not enabled, pretend to drive
        if self.debug > 1:
            time.sleep(time_in_sec)
            print '...done'
        else:
            self.drive_motor(self.FORWARD, self.SPEED)
            time.sleep(self.DRIVE_TIME)
            self.drive_motor(self.FORWARD, 0)
    
    # [Public] Drive backward for given time
    def drive_backward(self, time_in_sec):
        
        # If debug is on, print to console
        if self.debug > 0:
            print 'Driving backward'
            
        # If motors are not enabled, pretend to drive
        if self.debug > 1:
            time.sleep(time_in_sec)
            print '...done'
        else:
            self.drive_motor(self.BACKWARD, self.SPEED)
            time.sleep(self.DRIVE_TIME)
            self.drive_motor(self.FORWARD, 0)
    
    # [Public] Turn servo left and drive for given time 
    def drive_left(self, time_in_sec):
    
        # If debug is on, print to console
        if self.debug > 0:
            print 'Driving left'
            
        # If motors are not enabled, pretend to drive
        if self.debug > 1:
            time.sleep(time_in_sec)
            print '...done'
        else:
            self.drive_servo(self.LEFT)
            self.drive_motor(self.FORWARD, self.SPEED)
            time.sleep(self.STEER_TIME)
            self.drive_motor(self.FORWARD, 0)
            self.drive_servo(self.CENTER)
            
    # [Public] Turn servo right and drive for given time 
    def drive_right(self, time_in_sec):
        
        # If debug is on, print to console
        if self.debug > 0:
            print 'Driving right'
            
        # If motors are not enabled, pretend to drive
        if self.debug > 1:
            time.sleep(time_in_sec)
            print '...done'
        else:
            self.drive_servo(self.RIGHT)
            self.drive_motor(self.FORWARD, self.SPEED)
            time.sleep(self.STEER_TIME)
            self.drive_motor(self.FORWARD, 0)
            self.drive_servo(self.center)