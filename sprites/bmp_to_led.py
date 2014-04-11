# Bitmap files: Use 24-bit bitmap
BITMAP_FILES = ['face01.bmp', 'face02.bmp', 'face03.bmp', 'face04.bmp']

# Output text file
OUTPUT_FILE = 'ledmaps.txt'

# Constants
R = 0
G = 1
B = 2
NIBBLES_PER_BYTE = 2
BYTES_PER_PIXEL = 3

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

# Map 0-255 value to 0 - 3 LED value
def map_led(val):
    if (val <= 0):
        return 0
    if (val >= 1) and (val < 128):
        return 1
    if (val >= 128) and (val < 192):
        return 2
    if (val >= 192):
        return 3
       
# Open each bitmap file, translate to LED values, save to LED map file
out_file = open(OUTPUT_FILE, 'w')
for bmp_file in BITMAP_FILES:
       
    # Read bitmap data from file
    file = open(bmp_file, 'rb')
    data = file.read()
    file.close

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
            
    # Save LED map to file for lating reading
    out_file.write(str(led_matrix))
    out_file.write('\n')
    
# Close output file
out_file.close()

# Test - read file
with open(OUTPUT_FILE) as f:
    content = f.readlines()