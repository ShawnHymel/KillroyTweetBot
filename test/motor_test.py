import fcntl
import os
import time
from struct import *

# Constants
INPUT = '0'
OUTPUT = '1'
PWM_FREQ = 520

# Pin number
dir_pin = 8
pwm_pin = 5
pwm_value = 255

# File locations
MODE_FILE = '/sys/devices/virtual/misc/gpio/mode/gpio' + str(dir_pin)
PIN_FILE = '/sys/devices/virtual/misc/gpio/pin/gpio' + str(dir_pin)
PWM_FILE = '/dev/pwmtimer'

# Pin mode
os.system('echo ' + OUTPUT + ' > ' + MODE_FILE)

# Configure PWM
with open(PWM_FILE, 'wb') as f:
	pwm_struct = pack('iiiI', pwm_pin, 0, 0, PWM_FREQ)
	fcntl.ioctl(f, 0x107, pwm_struct)

# Motor control
def drive_motor(dir, pwm):
	
	# Set direction
	os.system('echo ' + str(dir) + ' > ' + PIN_FILE)

	# Output PWM to motor
	with open(PWM_FILE, 'wb') as f:
		pwm_struct = pack('ii', pwm_pin, pwm)
		fcntl.ioctl(f, 0x106, pwm_struct)

# Do stuff with the motor
drive_motor(0, 0)
time.sleep(1)
drive_motor(0, 200)
time.sleep(2)
drive_motor(0, 0)
time.sleep(0.5)
drive_motor(1, 255)
time.sleep(2)
drive_motor(0, 0)

