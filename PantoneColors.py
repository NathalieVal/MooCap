"""DAILY GAME PLAN:
    MAY 2nd: 
    Initialize pygame window
    Potentially figure out custom window sizing if it doesn't take too long just between fullscreen & windowed (https://www.youtube.com/watch?v=edJZOQwrMKw)
    BASIC windows & menus. Get buttons working.

    MAY 3RD:
    Figur out color randomizer system ( I have an idea in my head w/ a CSV file)"""

import pygame
import sys
import button

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init() # Initiates program
pygame.display.set_caption("Color Randomizer")

screen  = pygame.display.set_mode((1920, 1080)) # Initiates window

# Game Variables
game_menu = False

# Font(s)
font = pygame.font.SysFont("arialblack", 40)

# Font color(s)
text_col = (255, 255, 255)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Load Button Images
play_img = pygame.image.load('Buttons/Play.png').convert_alpha()
about_img = pygame.image.load('Buttons/About.png').convert_alpha()
exit_img = pygame.image.load('Buttons/Exit.png').convert_alpha()

# Create Button Instances
play_button = button.Button(100, 200, play_img, 1)
about_button = button.Button(100, 400, about_img, 1)
exit_button = button.Button(100, 600, exit_img, 1)


# Game Loop
run = True
while run:

    screen.fill((0, 0, 0))

    if play_button.draw(screen) == True:
        print("Play")
        
    if about_button.draw(screen) == True:
        print("About")

    if exit_button.draw(screen) == True:
        print("Exit")
        run = False


    # Check if menu button has been pressed
    if game_menu == True:
        pass
        # Display menu
    else: 
        draw_text("Press ESC to return to menu", font, text_col, 160, 250)

    # Event Handler
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            run = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game_menu = True
                print("Game Menu")

    pygame.display.update()
    clock.tick(60)