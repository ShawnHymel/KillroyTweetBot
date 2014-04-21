import serial

myPort = serial.Serial('/dev/ttyS1', 9600, timeout=10)

data = bytearray.fromhex(u'4A')
myPort.write(data)

myPort.close()
