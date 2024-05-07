import pygame


class NumericIndicator(pygame.sprite.Sprite):

    def __init__(self, posx, posy) -> None:
        super().__init__()
        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()

        self.number = 0
        self.font = pygame.font.Font("asset/font/digital-7.ttf", 30)
        self.text = f"{self.number}"
        self.image = self.font.render(self.text, True, pygame.Color(255, 255, 255))

        self.rect = self.image.get_rect()

        self.posx = posx
        self.posy = posy
        self.rect.centerx = self.posx
        self.rect.centery = self.posy


    def update(self, key_dict, fps, number):
        self.number = number
        self.text = f"{round(self.number)}"
        self.image = self.font.render(self.text, True, pygame.Color(255, 255, 255))
        self.rect = self.image.get_rect()
        
        self.rect.centerx = self.posx
        self.rect.centery = self.posy


        