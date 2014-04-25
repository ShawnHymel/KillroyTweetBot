import time
import pygame
import pygame.camera
from twython import Twython

# Twitter authentication 
APP_KEY = 'QP9zzvRZWgjDJkGgK8TZ6g'
APP_SECRET = 'wskPbXryJc1bHbESVmkYrfMHvsCVCty8LiEybvTAw'
OAUTH_TOKEN = '2366092298-Wg9ZNFm16QvTBO7LXCx3wGKknGgZKCoU1GFnyH7'
OAUTH_TOKEN_SECRET = 'wJgAcl4dYHGnDq8RcuUfV8fHzKLWlJ00XNR87Xg94qUXr'

# Connect to Twitter
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Initialize pygame
pygame.init()

# Initialize camera
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))

# Count down to picture shoot
print "Taking picture in..."
for i in range (0, 3):
    print str(3 - i)
    time.sleep(1)
print "CHEEEEEEESE!"

# Capture image and wait for image to write to disk
cam.start()
img = cam.get_image()
cam.stop()
pygame.image.save(img, 'image.jpg')
time.sleep(1)

# Post to Twitter
img = open('image.jpg')
#twitter.update_status(status="Why, hello world.")
twitter.update_status_with_media(status="More pics!", media=img)

# Capture image and wait for image to write to disk
cam.start()
img = cam.get_image()
cam.stop()
pygame.image.save(img, 'image.jpg')
time.sleep(1)

# Post to Twitter
img = open('image.jpg')
#twitter.update_status(status="Why, hello world.")
twitter.update_status_with_media(status="And more pics!", media=img)
