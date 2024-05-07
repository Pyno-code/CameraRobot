from math import pi
import pygame



class WidthIndicator(pygame.sprite.Sprite):
    
    
    def __init__(self) -> None:
        super().__init__()

        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()
        
        self.speed = 0.5 #mm
        self.ratio_padding_left = 0.60
        self.ratio_padding_bot = 0.1

        

        self.image = pygame.Surface((12, 12))
        self.image.fill(pygame.Color(255, 255, 255))

        self.rect = self.image.get_rect()

        self.rect.centerx = self.WIDTH/2
        self.rect.centery = (1 - self.ratio_padding_bot) * self.HEIGHT

        self.MAX_WIDTH = self.WIDTH/2 - self.WIDTH*self.ratio_padding_left/2 + self.rect.width/2
        self.MIN_WIDTH = self.WIDTH/2 + self.WIDTH*self.ratio_padding_left/2 - self.rect.width/2

    
    def move_back(self):
        if self.rect.centerx < self.MAX_WIDTH:
            self.rect.centerx = self.MAX_WIDTH
        if self.rect.centerx > self.MIN_WIDTH:
            self.rect.centerx = self.MIN_WIDTH

    def handle_input(self, key_dict, fps):
        if key_dict[pygame.K_q]:
            self.rect.x -= 1/fps*self.speed*self.MAX_WIDTH
        elif key_dict[pygame.K_d]:
            self.rect.x += 1/fps*self.speed*self.MAX_WIDTH


        if not (self.MIN_WIDTH > self.rect.centerx >= self.MAX_WIDTH):
            self.move_back()


    def update(self, key_dict, fps, *_):
        self.handle_input(key_dict, fps)



class HorizontalBar(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        self.ratio_padding_bot = 0.1

        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()

        self.image = pygame.image.load("asset/image/hud/vertical_bar.png")
        self.image = pygame.transform.rotate(self.image, 90)
        center = self.image.get_rect().center
        self.image = pygame.transform.smoothscale(self.image, (self.WIDTH*0.60, self.image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.center = center

        self.rect.centerx = self.WIDTH/2
        self.rect.centery = (1 - self.ratio_padding_bot) * self.HEIGHT
