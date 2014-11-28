### pagyme.py ###

import pygame
from pygame.locals import *
from pygame import surfarray
import sys

def quit(event):
    _continue = True
    if event.type == QUIT:
        _continue = False
    if (event.type == KEYDOWN) and (event.key == K_ESCAPE): _continue = False
    if (event.type == KEYDOWN) and (event.key == K_RETURN): _continue = False
    if _continue == False:
        pygame.quit()
        #sys.exit()
    return(_continue)

def show_stimulus(stimulus, name='toto', resizable=True):
    """
    stimulus is a 4 dimension numpy array: [height, weight, frame, RGB]
    """
    h = stimulus.shape[0]
    w = stimulus.shape[1]
    f = stimulus.shape[2]
    surfarray.use_arraytype('numpy')
    pygame.init()
    pygame.display.set_caption(name)
    if (resizable == True): screen = pygame.display.set_mode((h, w), RESIZABLE)
    else: screen = pygame.display.set_mode((h, w))
    surface = pygame.Surface((h, w))
    looping = True
    i = 0
    while looping:
        if (i == f): i = 0
        surfarray.blit_array(surface, stimulus[:, :, i, :])
        screen.blit(surface, (0, 0))
        pygame.display.flip()
        event = pygame.event.poll()
        looping = quit(event)
        i += 1
