from typing import Any
import pygame


class Crosshair(pygame.sprite.Sprite):

    def __init__(self) -> None:        
        super().__init__()

        self.speed = 75
        self.angle = 0

        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()
        self.image_start = pygame.image.load("asset/image/hud/crosshair.png")
        self.image_start = pygame.transform.smoothscale_by(self.image_start, 0.15)
        self.image = self.image_start.copy()
        self.rect = self.image.get_rect()

        self.rect.center = self.WIDTH/2, self.HEIGHT/2
        

    def update(self, key_dict, fps, *_) -> None:
        angle = 0
        if key_dict[pygame.K_c]:
            angle = 1/fps*self.speed
        elif key_dict[pygame.K_w]:
            angle = -1/fps*self.speed

        center = self.rect.center
        self.angle += angle
        self.image = pygame.transform.rotate(self.image_start, self.angle)

        self.rect = self.image.get_rect(center = center)



