import pygame
import pygame.camera
from pygame import PixelArray
import time

"""
camera init
"""
pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
cam.start()


screen = pygame.display.set_mode( (500, 500) )

i = 0;

while i < 10000:
    img = cam.get_image()
    screen.blit(img, (0, 0))
    pygame.display.flip()
    i += 1

# pygame.image.save(img, "picture.bmp")
pygame.camera.quit()
