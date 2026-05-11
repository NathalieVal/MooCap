import pygame

class Button():
    def __init__(self, x , y, image, image_hover, scale, click_sound=None):
        self.base_image = image
        self.base_hover_image = image_hover

        self.base_scale = scale
        self.current_scale = scale
        self.target_scale = scale

        self.animation_speed = 0.15

        self.hovered = False

        self.image = self.get_scaled_image()
        self.rect = self.image.get_rect(center=(x, y))

        self.clicked = False
        self.offset_x = 0 

        self.click_sound = click_sound

    def get_scaled_image(self):
        if self.hovered:
            source_image = self.base_hover_image
        else:
            source_image = self.base_image
        
        width = source_image.get_width()
        height = source_image.get_height()

        return pygame.transform.smoothscale(source_image,(int(width * self.current_scale),
                                                          int(height * self.current_scale)))


    def draw(self, surface):
        action = False
    
        # Get mouse position
        position = pygame.mouse.get_pos()

        # Check mouseover and clicked positions
        if self.rect.collidepoint(position[0] - self.offset_x, position[1]):
            self.hovered = True
            self.target_scale = self.base_scale * 1.1

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

                if self.click_sound:
                    self.click_sound.set_volume(0.2)
                    self.click_sound.play()

        else: 
            self.hovered = False
            self.target_scale = self.base_scale

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.current_scale += (self.target_scale - self.current_scale) * self.animation_speed

        center = self.rect.center

        self.image = self.get_scaled_image()

        self.rect = self.image.get_rect(center=center)
            

        # Draw button on screen
        surface.blit(self.image, (self.rect.x + self.offset_x, self.rect.y))
        
        return action
