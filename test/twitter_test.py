import time
#import RPi.GPIO as GPIO
from twython import TwythonStreamer

# Search terms
TERMS = '#yes'

# GPIO pin number of LED
LED = 22

# Twitter application authentication
APP_KEY = 'QP9zzvRZWgjDJkGgK8TZ6g'
APP_SECRET = 'wskPbXryJc1bHbESVmkYrfMHvsCVCty8LiEybvTAw'
OAUTH_TOKEN = '2366092298-OifRXA89kcRZ6lAcnsoDrLKDkeBk8ekumwzCQ9Y'
OAUTH_TOKEN_SECRET = 'Cy6dS5bYHzS3IwA82JhR4NtxlWfyihSebLZL4tFnZYNs5'

# Setup callbacks from Twython Streamer
class BlinkyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        print data['text'].encode('utf-8')
                        print
                        #GPIO.output(LED, GPIO.HIGH)
                        #time.sleep(0.5)
                        #GPIO.output(LED, GPIO.LOW)

# Setup GPIO as output
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(LED, GPIO.OUT)
#GPIO.output(LED, GPIO.LOW)

# Create streamer
try:
        stream = BlinkyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track=TERMS)
except KeyboardInterrupt:
        GPIO.cleanup()
