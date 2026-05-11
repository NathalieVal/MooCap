import pygame
import sys
import button
import csv
import random

pygame.init()

class Game:
    def __init__(self):

        self.screen  = pygame.display.set_mode((1920, 1080)) # Initiates window
        pygame.display.set_caption("Color Randomizer")

        # Loading Asset Images
        self.play_img = pygame.image.load('Gui/Buttons/Play.png').convert_alpha()
        self.playhover_img = pygame.image.load('Gui/Buttons/Play_HOVER.png').convert_alpha()
        self.randomcolor_img = pygame.image.load('Gui/Buttons/Random_Color.png').convert_alpha()
        self.randomcolorhover_img = pygame.image.load('Gui/Buttons/Random_Color_HOVER.png').convert_alpha()
        self.return_img = pygame.image.load('Gui/Buttons/Return.png').convert_alpha()
        self.returnhover_img = pygame.image.load('Gui/Buttons/Return_HOVER.png').convert_alpha()

        self.about_img = pygame.image.load('Gui/Buttons/About.png').convert_alpha()
        self.abouthover_img = pygame.image.load('Gui/Buttons/About_HOVER.png').convert_alpha()

        self.exit_img = pygame.image.load('Gui/Buttons/Exit.png').convert_alpha()
        self.exithover_img = pygame.image.load('Gui/Buttons/Exit_HOVER.png').convert_alpha()

        self.card_img = pygame.image.load('Gui/Card/Card.png').convert_alpha()

        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts 
        self.font = pygame.font.Font('Gui/Fonts/GrapeSoda.ttf', 40)

        # Game States
        self.game_state = "menu"

        # Scenes
        self.menu = MainMenu(self)
        self.randomizer = Randomizer(self)
        self.about = About(self)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        if self.game_state == "menu":
            self.menu.draw(self.screen)

        elif self.game_state == "play":
            self.randomizer.draw(self.screen)

        elif self.game_state == "about":
            self.about.draw(self.screen)
            

class MainMenu:
    def __init__(self, game):
        self.game = game

        self.play_button = button.Button(250, 200, game.play_img, game.playhover_img, 1)
        self.about_button = button.Button(250, 400, game.about_img, game.abouthover_img, 1)
        self.exit_button = button.Button(250, 600, game.exit_img, game.exithover_img, 1)   

    def handle_events(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen):
        screen.fill('white')

        if self.play_button.draw(screen) == True:
            self.game.game_state = "play"
            print("Play")
            
        if self.about_button.draw(screen) == True:
            print("About")
            self.game.game_state = "about"

        if self.exit_button.draw(screen) == True:
            print("Exit")
            self.game.running = False


class Randomizer:
    def __init__(self, game):
        self.game = game

        self.random_color = (0, 0, 0)
        self.color_text = []


        self.randomcolor_button = button.Button(250, 300, game.randomcolor_img, game.randomcolorhover_img, 1)
        self.return_button = button.Button(250, 500, game.return_img, game.returnhover_img, 1)

        self.card_img = game.card_img
        self.card_rect = self.card_img.get_rect(center=(960, 540))

        self.color_rect = pygame.Rect(0, 0, 455, 455)
        self.color_rect.center = (self.card_rect.centerx,
                                  self.card_rect.centery - 68)

    
    def draw(self, screen):
        screen.fill('white')
        
        if self.randomcolor_button.draw(screen):
            self.pick_color()

        if self.return_button.draw(screen):
            self.game.game_state = "menu"

        screen.blit(self.card_img, self.card_rect)
        pygame.draw.rect(screen, self.random_color, self.color_rect)

        for i, surface in enumerate(self.color_text):
            screen.blit(surface, (self.card_rect.left + 20,
                        self.card_rect.bottom - 140 + i * 50))
                
            
    def pick_color(self):
        with open('PantoneRGB.csv', 'r') as f:
            reader = csv.reader(f)
            random_row = random.choice(list(reader))

        name, code, r, g, b = random_row
        self.random_color = int(r), int(g), int(b)

        print(name, code, self.random_color)

        self.color_text = [
            self.game.font.render(name, True, 'black'),
            self.game.font.render(f"{self.random_color}", True, 'black'),
        ]


class About:
    def __init__(self, game):
        self.game = game

        self.return_button = button.Button(250, 500, game.return_img, game.returnhover_img, 1)

        about_data = [
            "ABOUT", 
            "", 
            "Developer: Nathalie Perez", 
            "", 
            "Art: Nathalie Perez",
            "", 
            "Audio: Pixabay"
        ]

        self.about_text = [game.font.render(line, True, 'black') 
                           for line in about_data]
        
    def draw(self, screen):
        screen.fill('white')

        for i, surface in enumerate(self.about_text):
            screen.blit(surface, (100, 100 + i * 50))

        if self.return_button.draw(screen):
            self.game.game_state = "menu"


if __name__ == "__main__":
    Game().run()
