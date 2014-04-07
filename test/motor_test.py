import fcntl
import os
import time
from struct import *

# Constants
INPUT = '0'
OUTPUT = '1'

# Pin number
pin = 12
pwm_pin = 5
pwm_value = 128

# File locations
MODE_FILE = '/sys/devices/virtual/misc/gpio/mode/gpio' + str(pin)
PIN_FILE = '/sys/devices/virtual/misc/gpio/pin/gpio' + str(pin)
PWM_FILE = '/dev/pwmtimer'

# Pin mode
os.system('echo ' + OUTPUT + ' > ' + MODE_FILE)

# Set direction
os.system('echo 1 > ' + PIN_FILE)

# Output PWM to motor
with open(PWM_FILE, 'wb') as f:
	pwm_struct = pack('ii', pwm_pin, pwm_value)
	fcntl.ioctl(f, 0x106, pwm_struct)
