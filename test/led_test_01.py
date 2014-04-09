# LED Matrix Test
#
# SPI0 CS - 10
# SPI0 MOSI - 11
# SPI0 MISO - 12
# SPI0 CLK - 13

import spi

data = [0x00, 0xe0, 0x1c, 0x03]
for i in range(0, 60):
	data.append(0x00)
data = tuple(data)
print 'Length: ' + str(len(data))

# Transfer data over SPI
spi.openSPI(speed=100000, mode=0, device='/dev/spidev0.0')
print spi.transfer(data)
spi.closeSPI()
