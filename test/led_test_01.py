# LED Matrix Test
#
# SPI0 CS - 10
# SPI0 MOSI - 11
# SPI0 MISO - 12
# SPI0 CLK - 13

import os
import spi

# Set pin modes
MODE = 2
MODE_FILE = '/sys/devices/virtual/misc/gpio/mode/gpio'
for i in range(10, 14):
	file = MODE_FILE + str(i)
	os.system('echo ' + str(MODE) + ' > ' + file)

# Init SPI
spi.openSPI(speed=100000, mode=0, device='/dev/spidev0.0')

# Initialize with number of boards
data = [0x25, 0x01] # Command and number of boards
print spi.transfer(tuple(data))

# Send Start of Frame
data = [0x26] # Start of frame
print spi.transfer(tuple(data))

# Send data
data = [0x01, 0x02, 0x03, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0xE4]
for i in range(0, 54):
	data.append(0x00)
#data = []
#for i in range(0, 64): # Clear
#	data.append(0x00)
print spi.transfer(tuple(data))

spi.closeSPI()
