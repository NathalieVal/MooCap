"""DAILY GAME PLAN:
    MAY 2nd: 
    Initialize pygame window
    Potentially figure out custom window sizing if it doesn't take too long just between fullscreen & windowed (https://www.youtube.com/watch?v=edJZOQwrMKw)
    BASIC windows & menus. Get buttons working.

    MAY 3RD:
    Figur out color randomizer system ( I have an idea in my head w/ a CSV file)"""

import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # Initiates program

WINDOW_SIZE = (400, 400)

screen  = pygame.display.set_mode(WINDOW_SIZE, 0, 32) # Initiates window

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)