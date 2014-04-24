import serial

myPort = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)

dir = 2            

hex_str = str(hex(dir))
hex_str = list(hex_str[2:])
if len(hex_str) < 2:
	hex_str.insert(0, '0')
hex_str = unicode("".join(hex_str))
data = bytearray.fromhex(hex_str)
#data = bytearray.fromhex(u'0')
myPort.write(data)

myPort.close()
