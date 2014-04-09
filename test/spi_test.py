#!/usr/bin/env python
import spi
## The openSPI() function is where the SPI interface is configured. 
## There are
##   three possible configuration options, and they all expect integer 
## values: speed - the clock speed in Hz mode - the SPI mode (0, 1, 2, 
## 3) bits - the length of each word, in bits (defaults to 8, which is 
## standard) It is also possible to pass a device name, but the default, 
## spidev0.0, is
##   the only device currently supported by the pcDuino.
## 
## SPI0 CS - 10
## SPI0 MOSI - 11
## SPI0 MISO - 12
## SPI0 CLK - 13
spi.openSPI(speed=100000, mode=0)
## Data is sent as a tuple, so you can construct a tuple as long as you 
## want
##   and the result will come back as a tuple of the same length.
print spi.transfer((0x0B, 0x02, 0x00))
## Finally, close the SPI connection. This is probably not necessary but 
## it's
##   good practice.
spi.closeSPI()
