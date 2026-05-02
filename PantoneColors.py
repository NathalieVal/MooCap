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
pygame.display.set_caption("Color Randomizer")

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_w]
screen  = pygame.display.set_mode((500, 500), pygame.RESIZABLE) # Initiates window

fullscreen = False

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == VIDEORESIZE:
            if not fullscreen:
                screen  = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE) # Initiates window


        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()  

            if event.key == K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((monitor_size), pygame.FULLSCREEN)
                else:
                    screen  = pygame.display.set_mode((screen.get_width, screen.get_height), pygame.RESIZABLE)

    pygame.display.update()
    clock.tick(60)