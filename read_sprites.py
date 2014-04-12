#-------------------------------------------------------------------------------
# Converts 8x8 (24-bit) bitmaps to text file with LED matrixc data
#
# Author: Shawn Hymel
# Date: April 12, 2014
# License: Beerware
#
# Reads 8x8 sprites from sprites/ directory and converts them to LED array
# values. These values are stored in a text file in the root directory of the
# project. They are needed by the main Kilroy script.
#-------------------------------------------------------------------------------

import os
import sys

#-------------------------------------------------------------------------------
# Constants
#-------------------------------------------------------------------------------

# Output file
OUTPUT_FILE = 'ledmaps.txt'

# Sprite dictionary keys and filenames (e.g. [<key>, <filename>] )
SPRITE_FILES = [['1 left', 'eye_1_left.bmp'], \
                ['1 right', 'eye_1_right.bmp'], \
                ['2 left', 'eye_2_left.bmp'], \
                ['2 right', 'eye_2_right.bmp'], \
                ['3 left', 'eye_3_left.bmp'], \
                ['3 right', 'eye_3_right.bmp'], \
                ['closed left', 'eye_closed_left.bmp'], \
                ['closed right', 'eye_closed_right.bmp'], \
                ['open left', 'eye_open_left.bmp'], \
                ['open right', 'eye_open_right.bmp']]
     
# Global constants    
NIBBLES_PER_BYTE = 2
BYTES_PER_PIXEL = 3 
R = 0
G = 1
B = 2
                
#-------------------------------------------------------------------------------
# Functions
#-------------------------------------------------------------------------------

# Flip endian of string byte array (hex)
def flip_endian(str_num):

    # Check if  is not even length (bytes)
    if len(str_num) % 2 != 0:
        return -1
        
    # Swap byte order
    num_bytes = len(str_num) / 2
    ans = ''
    for b in range(0, num_bytes):
        i = num_bytes - b - 1
        ans = ans + str_num[(2*i):((2*i) + 2)]
        
    return ans

# Map 0-255 bitmap value to 0 - 3 LED value
def map_led(val):
    if (val <= 0):
        return 0
    if (val >= 1) and (val < 128):
        return 1
    if (val >= 128) and (val < 192):
        return 2
    if (val >= 192):
        return 3

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------

def main():

    # Create blank dictionary
    led_dict = {}

    #***TEST
    key_name = '1 left'
    
    # Create array from each bitmap file
    for bmp_file in SPRITE_FILES:

        # Open file
        file_path = 'sprites/' + bmp_file[1]
        fn = os.path.join(os.path.dirname(__file__), file_path)
        fd = open(fn, 'rb')
        data = fd.read()
        fd.close()
        
        # Parse data
        data = bytearray(data)
        width = ''.join(format(x, '02x') for x in data[18:22])
        height = ''.join(format(x, '02x') for x in data[22:26])
        bitmap = ''.join(format(x, '02x') for x in data[54:])

        # Find width and height
        width = flip_endian(width)
        width = int(width, 16)
        height = flip_endian(height)
        height = int(height, 16)

        # Check to make sure bitmap is 8x8
        if (width != 8) or (height != 8):
            print 'ERROR: Bitmap ' + bmp_file + ' is not 8x8 pixels'
            exit()

        # Find padding in bytes
        pad = width % 4

        # Strip padding from bitmap data
        led_string = ''
        nib_in_img_width = (width * BYTES_PER_PIXEL * NIBBLES_PER_BYTE)
        nib_in_row = nib_in_img_width + (pad * NIBBLES_PER_BYTE)
        for i, c in enumerate(bitmap):
            if ((i % nib_in_row) < nib_in_img_width):
                led_string = led_string + c
            
        # Flip endian-ness of array
        led_string = flip_endian(led_string)

        # Construct blank LED matrix
        led_matrix = []
        for y in range(0, height):
            led_matrix.append([])
            for x in range(0, width):
                led_matrix[y].append([])
                
        # Fill matrix with integer data from bitmap data
        pix_num = 0
        for y in range(0, height):
            for x in range(0, width):
                
                # Calculate index into bitmap array
                byte_num = ((y * width) + x) * BYTES_PER_PIXEL
                
                # Set RED value
                byte_val = led_string[(byte_num + R) * 2] + \
                            led_string[((byte_num + R) * 2) + 1]
                led_matrix[y][x].append(map_led(int(byte_val, 16)))
                
                # Set GREEN value
                byte_val = led_string[(byte_num + G) * 2] + \
                            led_string[((byte_num + G) * 2) + 1]
                led_matrix[y][x].append(map_led(int(byte_val, 16)))
                
                # Set BLUE value
                byte_val = led_string[(byte_num + B) * 2] + \
                            led_string[((byte_num + B) * 2) + 1]
                led_matrix[y][x].append(map_led(int(byte_val, 16)))
                
        # Add array to dictionary with keyname
        led_dict[bmp_file[0]] = led_matrix
            
    # Write dictionary to file
    out_file = open(OUTPUT_FILE, 'w')
    out_file.write(str(led_dict))
    out_file.close()

# Run main
main()
