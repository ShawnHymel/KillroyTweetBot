import time
import pygame
import pygame.camera
from pygame.locals import *

# Initialize pygame
pygame.init()

# Initialize camera
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()

# Capture image
image = cam.get_image()
pygame.image.save(image, "image.jpg")

# Get width and height of image
img_width = image.get_width()
img_height = image.get_height()
print str(img_width) + " x " + str(img_height)

# Display image
screen = pygame.display.set_mode( (img_width, img_height) )
pygame.display.set_caption("Camera View")

# Wait for exit
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

    # Draw frame
    screen.blit(image, (0,0))
    pygame.display.flip()
    image = cam.get_image()
