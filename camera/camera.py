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

def pa_compare(array, original):
    # w, h   = array.shape
    # w0, h0 = original.shape
    # if (w != w0): return -1
    # if (h != h0): return -1

    dist = 0
    maxx = -1
    maxy = -1
    for x, row in enumerate(array):
        if maxx < x: maxx = x
        for y, pixel in enumerate(row):
            if maxy < y: maxy = y
            dist += abs(pixel - original[x, y])

    return dist / float(x / y)


for i in xrange(50):
    img = cam.get_image()

img = cam.get_image()
first = PixelArray(img)

while True:
    img = cam.get_image()
    pa = PixelArray(img)
    # compared = first.compare(pa)
    # img = compared.make_surface()
    # pygame.image.save(img, "screenshot.bmp")
    print pa_compare(pa, first)
    img = pa.make_surface()
    time.sleep(0.05)
    screen.blit(img, (0, 0));
    pygame.display.flip()
    # time.sleep(0.25)

pygame.camera.quit()
