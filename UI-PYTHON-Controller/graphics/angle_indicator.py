
import pygame


class AngleIndicator(pygame.sprite.Sprite):

    def __init__(self, left=True) -> None:
        super().__init__()
        
        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()
        self.ratio_padding_left = 0.12
        
        self.image = pygame.image.load("asset/image/hud/angle_bar.png")
        self.image = pygame.transform.smoothscale(self.image, (self.image.get_width() * 0.65, self.image.get_height() * 0.90))
        self.rect = self.image.get_rect()
        self.rect.x = self.WIDTH*self.ratio_padding_left
        self.rect.centery = self.HEIGHT/2

        if not left:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.right = self.WIDTH*(1-self.ratio_padding_left)




        