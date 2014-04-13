import os
import spi
import time

LEDMAP_FILE = 'ledmaps.txt'

# Read file
led_file = open(LEDMAP_FILE, 'r')
content = led_file.read()
led_file.close()
led_dict = eval(content)

print led_dict['1 left']

# Set pin modes
MODE = 2
MODE_FILE = '/sys/devices/virtual/misc/gpio/mode/gpio'
for i in range(10, 14):
        file = MODE_FILE + str(i)
        os.system('echo ' + str(MODE) + ' > ' + file)

# Init SPI
spi.openSPI(speed=100000, mode=0, device='/dev/spidev0.0')

# Initialize wtih number of boards
#data = [0x25, 0x01]
#spi.transfer(tuple(data))

# Clear LED matrix
data = [0x26]
spi.transfer(tuple(data))
data = []
for i in range(0, 64):
        data.append(0x00)
spi.transfer(tuple(data))
time.sleep(0.01)
spi.transfer(tuple(data))

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['open right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['open left']))

# Delay
time.sleep(1)

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['closed right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['closed left']))

# Delay
time.sleep(0.5)

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['open right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['open left']))

# Delay
time.sleep(1)

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['3 right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['3 left']))

# Delay
time.sleep(1)

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['2 right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['2 left']))

# Delay
time.sleep(1)

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['1 right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['1 left']))

# Delay
time.sleep(1)

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['camopen right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['camopen left']))

# Delay
time.sleep(0.5)

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['camclose right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['camclose left']))

# Delay
time.sleep(0.5)

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['camopen right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['camopen left']))

# Delay
time.sleep(0.5)

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['heart right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['heart left']))

# Delay
time.sleep(2)

# Send ledmap
data = [0x26]
spi.transfer(tuple(data))
spi.transfer(tuple(led_dict['open right']))
time.sleep(0.01)
spi.transfer(tuple(led_dict['open left']))

# Close SPI
spi.closeSPI()