import os
import time

# Constants
INPUT = '0'
OUTPUT = '1'

# Pin number
pin = 10

# File locations
MODE_FILE = '/sys/devices/virtual/misc/gpio/mode/gpio' + str(pin)
PIN_FILE = '/sys/devices/virtual/misc/gpio/pin/gpio' + str(pin)

# Pin mode
os.system('echo ' + OUTPUT + ' > ' + MODE_FILE)

# Blink!
while True:
	os.system('echo 1 > ' + PIN_FILE)
	time.sleep(0.5)
	os.system('echo 0 > ' + PIN_FILE)
	time.sleep(0.5)
