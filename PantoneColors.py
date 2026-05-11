import pygame
import sys
import button
import csv
import random

pygame.init()


class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.next_scene = None

        self.state = "idle"

        self.offset_x = 0
        self.speed = 50

        self.progress = 0
        self.direction = -1

    def set_scene(self, scene):
        if self.current_scene is None:
            self.current_scene = scene
            self. state = "idle"
            return
        
        self.next_scene = scene
        self.state = "transition"
        self.progress = 0
        self.direction = -1

    def ease(self, t):
        return t * t * (3 - 2 * t)

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self):
        if self.current_scene is None:
            return
        
        if self.state == "idle":
            self.current_scene.update()
            return

        if self.state == "transition":
            self.progress += 0.02 # Speed

            if self.progress >= 1:
                self.progress = 1
                self.current_scene = self.next_scene
                self.next_scene = None
                self.state = "fade_in"
                return 

        if self.state == "fade_in":
            self.progress -= 0.03 # Speed

            if self.progress <= 0:
                self.progress = 0
                self.state = "idle"
            
    def draw(self, screen):
        if self.current_scene is None:
            return
        
        t = self.ease(self.progress)

        offset = 0

        if self.state == "transition":
            offset = -int(t * 1920)

        elif self.state =="fade_in":
            alpha = -int((1 - t) * 1920)

        self.current_scene.draw(screen, offset)

        if self.state != "idle":
            fade = pygame.Surface((1920, 1080))
            fade.fill((255, 255, 255))
            alpha = int(abs(t - 0.5) * 2 * 255)
            fade.set_alpha(alpha)
            screen.blit(fade, (0, 0))


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
        self.scene_manager = SceneManager()

        # Scenes
        self.menu_scene = MainMenu(self)
        self.randomizer_scene = Randomizer(self)
        self.about_scene = About(self)

        self.scene_manager.set_scene(self.menu_scene)

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
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

        self.scene_manager.handle_events(events)

    def update(self):
        self.scene_manager.update()

    def draw(self):
        self.scene_manager.draw(self.screen)
            

class Scene:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen, offset_x=0):
        pass


class MainMenu(Scene):
    def __init__(self, game):
        self.game = game

        self.play_button = button.Button(250, 200, game.play_img, game.playhover_img, 1)
        self.about_button = button.Button(250, 400, game.about_img, game.abouthover_img, 1)
        self.exit_button = button.Button(250, 600, game.exit_img, game.exithover_img, 1)   

    def handle_events(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen, offset_x=0):
        screen.fill('white')

        self.play_button.offset_x = offset_x
        self.about_button.offset_x = offset_x
        self.exit_button.offset_x = offset_x

        if self.play_button.draw(screen) == True:
            self.game.scene_manager.set_scene(self.game.randomizer_scene)
            
        if self.about_button.draw(screen) == True:
            self.game.scene_manager.set_scene(self.game.about_scene)

        if self.exit_button.draw(screen) == True:
            self.game.running = False


class Randomizer(Scene):
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

    
    def draw(self, screen, offset_x):
        screen.fill('white')

        self.randomcolor_button.offset_x = offset_x
        self.return_button.offset_x = offset_x
        
        if self.randomcolor_button.draw(screen):
            self.pick_color()

        if self.return_button.draw(screen):
            self.game.scene_manager.set_scene(self.game.menu_scene)

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

    def handle_events(self, events):
        for event in events:
            pass


class About(Scene):
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
        
    def draw(self, screen, offset_x):
        screen.fill('white')

        self.return_button.offset_x = offset_x

        for i, surface in enumerate(self.about_text):
            screen.blit(surface, (100, 100 + i * 50))

        if self.return_button.draw(screen):
            self.game.scene_manager.set_scene(self.game.menu_scene)


if __name__ == "__main__":
    Game().run()
