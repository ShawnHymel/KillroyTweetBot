import os
import spi
import time

LEDMAP_FILE = 'ledmaps.txt'

# Create list of bytes for LED matrix
def str_to_led(led_str):

    # Create list of strings for LED matrix
    led_out = []
    ledmap = []
    i = 0
    pix_str = ''
    for n in led_str:
        if n.isdigit():
            pix_str = pix_str + n
            if (i % 3 == 2):
                ledmap.append(pix_str)
                pix_str = ''
            i = i + 1

    # Convert list of strings to bytes for LED matrix
    for n in ledmap:
        r_val = ((1 << 4) << int(n[0])) & 0xe0
        g_val = ((1 << 1) << int(n[1])) & 0x1c
        b_val = int(n[2])
        pix_val = r_val + g_val + b_val
        led_out.append(pix_val)

    return led_out

# Read file
with open(LEDMAP_FILE) as f:
    content = f.read().splitlines()

# Translate strings to LED values
led_out = []
for s in content:
    led_out.append(str_to_led(s))

# Set pin modes
MODE = 2
MODE_FILE = '/sys/devices/virtual/misc/gpio/mode/gpio'
for i in range(10, 14):
        file = MODE_FILE + str(i)
        os.system('echo ' + str(MODE) + ' > ' + file)

# Init SPI
spi.openSPI(speed=100000, mode=0, device='/dev/spidev0.0')

# Initialize wtih number of boards
data = [0x25, 0x01]
spi.transfer(tuple(data))

# Clear LED matrix
data = [0x26]
spi.transfer(tuple(data))
data = []
for i in range(0, 64):
        data.append(0x00)
spi.transfer(tuple(data))

for i in range(0, 10):

    # Send ledmap (smiley)  data
    data = [0x26]
    spi.transfer(tuple(data))
    spi.transfer(tuple(led_out[0]))

    # Delay
    time.sleep(1)

    # Send ledmap (blink) data
    data = [0x26]
    spi.transfer(tuple(data))
    spi.transfer(tuple(led_out[1]))

    # Delay
    time.sleep(0.5)

# Close SPI
spi.closeSPI()
