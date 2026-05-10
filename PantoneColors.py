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

screen  = pygame.display.set_mode((1920, 1080)) # Initiates window

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, x, y)


# Game Loop
run = True
while run:

    screen.fill((0, 0, 0))


    # Event Handler
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            run = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()  
                run = False

    pygame.display.update()
    clock.tick(60)