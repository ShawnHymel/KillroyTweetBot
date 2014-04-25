import time
import pygame
import pygame.camera
from pygame.locals import *

# Initialize pygame
pygame.init()

# Initialize camera
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video1",(640,480))
cam.start()

# Capture image
image = cam.get_image()
pygame.image.save(image, "image1.jpg")
cam.stop()

# Capture image
cam.start()
image = cam.get_image()
pygame.image.save(image, "image2.jpg")
cam.stop
