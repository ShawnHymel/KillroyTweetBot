import os
#import spi
import time

LEDMAP_FILE = 'ledmaps.txt'

# Create list of bytes for LED matrix
def map_to_led(led_val):

    # Convert list of strings to bytes for LED matrix
    led_out = []
    for y in led_val:
        for n in y:
            r_val = ((1 << 4) << int(n[0])) & 0xe0
            g_val = ((1 << 1) << int(n[1])) & 0x1c
            b_val = int(n[2])
            pix_val = r_val + g_val + b_val
            led_out.append(pix_val)

    return led_out

# Read file
led_file = open(LEDMAP_FILE, 'r')
content = led_file.read()
led_file.close()
led_dict = eval(content)

# Translate dictionary values to LED values
#for k, val in led_dict:
#    led_dict[k] = map_to_led(val)

print map_to_led(led_dict['1 left'])
   
#led_out = []
#for s in content:
#    led_out.append(str_to_led(s))

# Set pin modes
#MODE = 2
#MODE_FILE = '/sys/devices/virtual/misc/gpio/mode/gpio'
#for i in range(10, 14):
#        file = MODE_FILE + str(i)
#        os.system('echo ' + str(MODE) + ' > ' + file)

# Init SPI
#spi.openSPI(speed=100000, mode=0, device='/dev/spidev0.0')

# Initialize wtih number of boards
#data = [0x25, 0x01]
#spi.transfer(tuple(data))

# Clear LED matrix
#data = [0x26]
#spi.transfer(tuple(data))
#data = []
#for i in range(0, 64):
#        data.append(0x00)
#spi.transfer(tuple(data))

#for i in range(0, 10):
#
#    # Send ledmap (smiley)  data
#    data = [0x26]
#    spi.transfer(tuple(data))
#    spi.transfer(tuple(led_out[0]))

    # Delay
#    time.sleep(1)

    # Send ledmap (blink) data
#    data = [0x26]
#    spi.transfer(tuple(data))
#    spi.transfer(tuple(led_out[1]))

    # Delay
#    time.sleep(0.5)

# Close SPI
#spi.closeSPI()
