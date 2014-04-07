import fcntl
from struct import *

PWM_FILE = '/dev/pwmtimer'

pwm_pin = 5
pwm_value = 128

with open(PWM_FILE, 'wb') as f:
	pwm_struct = pack('ii', pwm_pin, pwm_value)
	fcntl.ioctl(f, 0x106, pwm_struct)
