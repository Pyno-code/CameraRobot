import time
from typing import Any
import pygame


class CompassIndicator(pygame.sprite.Sprite):
    


    def __init__(self) -> None:
        super().__init__()
        
        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()

        self.ratio_padding_top = 0.04
 
        self.speed = 5
        self.angle = 180
        self.number_figures = 11
        self.step = 5
        self.penta_angle = round(self.angle/5)*5

        self.image = pygame.Surface((self.WIDTH*0.75, 100), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()

        self.vertical_bar = pygame.Rect(0, 0, 2, 40)
        self.vertical_bar_diff = 4
        
        self.rect.x = abs(self.WIDTH - self.rect.width)/2
        self.rect.y = self.HEIGHT * self.ratio_padding_top

        min_value = int(self.penta_angle - int((self.number_figures)/2) * self.step)
        self.values = [i for i in range(min_value, min_value + self.step * (self.number_figures), self.step)]


    def update(self, key_dict, fps, *_) -> None:
        self.handle_input(key_dict, fps)
        self.penta_angle = round(self.angle/5)*5

        self.image.fill((0, 0, 0, 0))

        for value in range(self.number_figures):
            angle_diff = self.angle - (self.penta_angle - (self.number_figures // 2 - value) * self.step)
            height = int(self.vertical_bar.height - 30*(1-abs(angle_diff/40)))
            surface = pygame.Surface((self.vertical_bar.width, height))
            surface.fill((255, 255, 255))

            # Calculate position based on angle difference
            position_x = self.rect.width / 2 + angle_diff / 180 * 5000
            position_y = self.rect.height / 2 - height / 2

            self.image.blit(surface, (position_x, position_y))

    def handle_input(self, key_dict, fps):
        if key_dict[pygame.K_a]:
            self.angle -= 1/fps*self.speed
        elif key_dict[pygame.K_e]:
            self.angle += 1/fps*self.speed

        self.angle = self.angle % 360
        if self.angle < 0:
            self.angle = 360 - self.angle



class PointerIndicator(pygame.sprite.Sprite):

    def __init__(self, down=True) -> None:
        super().__init__()
        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()

        self.image = pygame.image.load("asset\image\hud\pointer.png")
        self.ratio_padding_top = 0.08

        if not down:
            self.image = pygame.transform.flip(self.image, False, True)
            self.ratio_padding_top = 0.1125

        self.rect = self.image.get_rect()

        self.rect.centerx = self.WIDTH/2
        self.rect.y = self.HEIGHT*self.ratio_padding_top

