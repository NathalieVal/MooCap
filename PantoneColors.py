import pygame
import sys
import csv
import random
import webbrowser
import button


pygame.init()
pygame.mixer.init()

class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.next_scene = None
        self.state = "idle"
        self.progress = 0

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
        
        self.progress += 0.02 # Speed

        if self.state == "transition":
            if self.progress >= 1:
                self.progress = 0
                self.current_scene = self.next_scene
                self.next_scene = None
                self.state = "fade_in"
                return 

        if self.state == "fade_in":

            if self.progress >= 1:
                self.progress = 0
                self.state = "idle"
            
    def draw(self, screen):
        if self.current_scene is None:
            return
        
        t = self.ease(self.progress)

        offset = 0

        if self.state == "transition":
            offset = -int(t * 1920)

        self.current_scene.draw(screen, offset)

        if self.state in ("transition", "fade_in"):
            fade = pygame.Surface((1920, 1080))
            fade.fill((255, 255, 255))

            if self.state == "transition":
                alpha = int(t * 255)
            else:
                alpha = int((1 - t) * 255)

            fade.set_alpha(alpha)
            screen.blit(fade, (0, 0))


class Scene:

    """THIS IS A TEMPLATE FOR SCENES
    Some scenes use all functions and some don't.
    Empty functions can be deleted but I like how consistent they look with every function.
    In future decisions they can come in handy so I prefer to leave them.

    """

    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen, offset_x=0):
        pass


class Main:
    def __init__(self):
        self.screen  = pygame.display.set_mode((1250, 1080)) # Initiates window
        pygame.display.set_caption("Color Randomizer")

        # Loading Asset Images
        self.logo_img = pygame.image.load('Gui/Intro.png').convert_alpha()

        self.play_img = pygame.image.load('Gui/Buttons/Play.png').convert_alpha()
        self.playhover_img = pygame.image.load('Gui/Buttons/Play_HOVER.png').convert_alpha()

        self.randomcolor_img = pygame.image.load('Gui/Buttons/Random_Color.png').convert_alpha()
        self.randomcolorhover_img = pygame.image.load('Gui/Buttons/Random_Color_HOVER.png').convert_alpha()

        self.return_img = pygame.image.load('Gui/Buttons/Return.png').convert_alpha()
        self.returnhover_img = pygame.image.load('Gui/Buttons/Return_HOVER.png').convert_alpha()

        self.about_img = pygame.image.load('Gui/Buttons/About.png').convert_alpha()
        self.abouthover_img = pygame.image.load('Gui/Buttons/About_HOVER.png').convert_alpha()

        self.credits_img = pygame.image.load('Gui/Credits.png').convert_alpha()
        self.meme_img = pygame.image.load('Gui/Meme.png').convert_alpha()

        self.exit_img = pygame.image.load('Gui/Buttons/Exit.png').convert_alpha()
        self.exithover_img = pygame.image.load('Gui/Buttons/Exit_HOVER.png').convert_alpha()

        #SFX 
        pygame.mixer.music.load('SFX/BackgroundMusic.mp3')
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        self.click_sound = pygame.mixer.Sound('SFX/ButtonPress.mp3')
        self.card_sound = pygame.mixer.Sound('SFX/Card.mp3')
        

        self.card_img = pygame.image.load('Gui/Card/Card.png').convert_alpha()

        self.clock = pygame.time.Clock()
        self.running = True

        # Fonts 
        self.font = pygame.font.Font('Gui/Fonts/GrapeSoda.ttf', 40)

        # Game States
        self.scene_manager = SceneManager()

        # Scenes
        self.intro_scene = Intro(self)
        self.menu_scene = MainMenu(self)
        self.randomizer_scene = Randomizer(self)
        self.about_scene = About(self)

        self.scene_manager.set_scene(self.intro_scene)

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
            

class Intro(Scene):
    def __init__(self, game):
        self.game = game

        self.logo_img = game.logo_img
        self.logo_rect = self.logo_img.get_rect(center=(625, 540))

        self.timer = 0

        self.fade_in_time = 120
        self.hold_time = 80
        self.fade_out_time = 120

        self.total_time = (self.fade_in_time + self.hold_time + self.fade_out_time)

        self.finished = False

    def handle_events(self, events):
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.finished):
                    self.finished = True
                    self.game.scene_manager.set_scene(self.game.menu_scene)


    def update(self):
        self.timer += 1

        if self.timer >= self.total_time and not self.finsihed:
            self.finished = True
            self.game.scene_manager.set_scene(self.game.menu_scene)

    def draw(self, screen, offset_x=0):
        screen.fill('white')

        alpha = 255

        if self.timer < self.fade_in_time:
            alpha = int((self.timer / self.fade_in_time) * 255)

        elif self.timer < (self.fade_in_time + self.hold_time):
            alpha = 255

        else: 
            self.fade_out_timer = (self.timer - self.fade_in_time - self.fade_out_time)

            alpha = int(255 - (self.fade_out_timer / self.fade_out_time) * 255)


        # self.logo_placeholder = pygame.Surface ((200, 200))
        # self.logo_placeholder.set_colorkey((0, 0, 0))
        # self.logo_placeholder.set_alpha(alpha)
        # pygame.draw.circle(self.logo_placeholder, (0, 0, 255), (100, 100), 100)
        # screen.blit(self.logo_placeholder, (625, 540))

        intro_logo = self.logo_img.copy()
        intro_logo.set_alpha(alpha)

        screen.blit(intro_logo, self.logo_rect)


class MainMenu(Scene):
    def __init__(self, game):
        self.game = game

        self.play_button = button.Button(300, 340, game.play_img, game.playhover_img, 1, game.click_sound)
        self.about_button = button.Button(300, 540, game.about_img, game.abouthover_img, 1, game.click_sound)
        self.exit_button = button.Button(300, 740, game.exit_img, game.exithover_img, 1, game.click_sound)   

        self.logo_img = game.logo_img
        self.logo_rect = self.logo_img.get_rect(center=(850, 540))

    def handle_events(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen, offset_x=0):
        screen.fill('white')

        screen.blit(self.logo_img, self.logo_rect)

        self.play_button.offset_x = offset_x
        self.about_button.offset_x = offset_x
        self.exit_button.offset_x = offset_x

        if self.play_button.draw(screen) == True:
            self.game.scene_manager.set_scene(self.game.randomizer_scene)
            
        if self.about_button.draw(screen) == True:
            self.game.scene_manager.set_scene(self.game.about_scene)

        if self.exit_button.draw(screen) == True:
            self.game.running = False


class ColorCard:
    def __init__(self, image, color, color_text, color_name, target_positon):
        self.image = image
        self.color = color

        self.color_text = color_text
        self.color_name = color_name

        self.x, self.y = target_positon[0], -700
        self.target_x, self.target_y = target_positon

        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.color_rect = pygame.Rect(0, 0, 455, 455)

        self.text_rects = []


        self.link = f"https://www.pantone.com/color-finder/{color_name[0].replace(' ', '-')}"

    def handle_events(self, events):
        pass

    def update(self):
        self.y += (self.target_y - self.y) * 0.15
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        self.color_rect.center = (self.rect.centerx, self.rect.centery - 70)

        screen.blit(self.image,self.rect)
        pygame.draw.rect(screen, self.color, self.color_rect)

        self.text_rects = []
        mouse_position = pygame.mouse.get_pos()

        for i, surface in enumerate(self.color_text):
            position = (self.rect.left + 20,
                        self.rect.bottom - 140 + i * 50)
            
            rect = surface.get_rect(topleft=position)
            self.text_rects.append(rect)
                
            screen.blit(surface, position)



class Randomizer(Scene):
    def __init__(self, game):
        self.game = game

        self.randomcolor_button = button.Button(300, 440, game.randomcolor_img, game.randomcolorhover_img, 1, game.click_sound)
        self.return_button = button.Button(300, 640, game.return_img, game.returnhover_img, 1, game.click_sound)

        self.card_img = game.card_img
        self.cards = []
        
    def handle_events(self, events):
        mouse_position = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for card in reversed(self.cards):
                        for rect in card.text_rects:
                            if rect.collidepoint(mouse_position):
                                webbrowser.open(card.link)
                                return

    def update(self):
        for card in self.cards:
            card.update()

    
    def draw(self, screen, offset_x):
        screen.fill('white')

        self.randomcolor_button.offset_x = offset_x
        self.return_button.offset_x = offset_x
        
        if self.randomcolor_button.draw(screen):
            self.pick_color()

        if self.return_button.draw(screen):
            self.game.scene_manager.set_scene(self.game.menu_scene)

        for card in self.cards:
            card.draw(screen)
                
            
    def pick_color(self):
        with open('PantoneRGB.csv', 'r') as f:
            reader = csv.reader(f)
            random_row = random.choice(list(reader))

        name, code, r, g, b = random_row
        self.random_color = int(r), int(g), int(b)

        self.text_data = [f"PANTONE {name}",
                          f"{self.random_color}"]

        self.text_color = [
            self.game.font.render(self.text_data[0], True, 'black'), 
            self.game.font.render(self.text_data[1], True, 'black')]

        self.new_card = ColorCard(self.card_img, 
                                self.random_color, 
                                self.text_color,
                                [name, name],
                                (850, 475))

        self.cards.append(self.new_card)

        self.game.card_sound.set_volume(0.7)
        self.game.card_sound.play()

        for i, card in enumerate(self.cards):
            card.target_y = 475 + i * 18

        if len(self.cards) > 5:
            self.cards.pop(0)


class About(Scene):
    def __init__(self, game):
        self.game = game

        self.credits_img = game.credits_img
        self.meme_img = game.meme_img

        self.return_button = button.Button(300, 640, game.return_img, game.returnhover_img, 1, game.click_sound)

    def handle_events(self, event):
        pass
    
    def update(self):
        pass

    def draw(self, screen, offset_x):
        screen.fill('white')
        
        screen.blit(self.credits_img, (125, 200))
        screen.blit(self.meme_img, (600, 400))

        self.return_button.offset_x = offset_x

        if self.return_button.draw(screen):
            self.game.scene_manager.set_scene(self.game.menu_scene)


if __name__ == "__main__":
    Main().run()