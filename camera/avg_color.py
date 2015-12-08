import pygame
import pygame.camera
import numpy
from pygame import PixelArray
import time
from collections import deque
import sys
import time

TRAINING_ITERATIONS = 10
LIFETIME = 100
BUFFER_LENGTH = 5


"""
camera init
"""
pygame.camera.init()
cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
cam.start()

# find average color currently in camera 
def average_color(cam):
    array = PixelArray(cam.get_image())
    total = sum(map(sum, array)) / sum([ len(row) for row in array ])
    del array
    return total

# finds an average color for the frame
def train(cam):
    print 'TRAINING STILLNESS . . .',
    avg = 0
    for i in xrange(TRAINING_ITERATIONS):
        print '.',
        sys.stdout.flush()
        avg += average_color(cam)
    avg /= TRAINING_ITERATIONS
    print ' DONE.'
    print 'TRAINING DISRUPTION . . .' ,

    buf = deque()
    minimum = float('inf')
    variances = []
    for i in xrange(TRAINING_ITERATIONS + BUFFER_LENGTH):
        delta = abs(average_color(cam) - avg)

        buf.append(delta)
        if (i < BUFFER_LENGTH): continue
        buf.popleft()

        variances.append(numpy.var(buf))
        # if var < minimum:
        #     minimum = var

        print '.',
        sys.stdout.flush()


    print 'DONE.'
    print variances
    print numpy.average(variances)
    print numpy.std(variances)
    return (avg / TRAINING_ITERATIONS, numpy.average(variances) - numpy.std(variances))


AVERAGE, THRESHOLD = train(cam)

buf = deque()

disrupted = 0

print 'OK, BEGIN.'
for i in xrange(LIFETIME):
    delta = abs(average_color(cam) - AVERAGE)

    buf.append(delta)
    if (i < BUFFER_LENGTH): continue
    buf.popleft()

    if numpy.var(buf) > THRESHOLD:
        disrupted += 1
        print '\033[91mDISRUPTION:\033[0m',
        if disrupted % BUFFER_LENGTH == 1:
            print 'saving.',
            img = cam.get_image()
            pygame.image.save(img, "./db/" + str(int(time.time())) + '.bmp')
        print ''

        sys.stdout.flush() 
    else:
        if disrupted != 0:
            print '\033[92mALL CLEAR\033[0m'
        disrupted = 0 
    # else:
    #     print '\033[92mALL CLEAR\033[0m'

pygame.camera.quit()
