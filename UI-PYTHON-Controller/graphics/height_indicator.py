import pygame



class HeightIndicator(pygame.sprite.Sprite):
    
    
    def __init__(self, side: bool = True) -> None:
        super().__init__()

        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()
        

        self.speed = 0.5 #mm
        self.ratio_padding_left = 0.08
        self.ratio_padding_bot = 0.18

        self.MAX_HEIGHT = self.HEIGHT*self.ratio_padding_bot + 50
        self.MIN_HEIGHT = self.HEIGHT - self.MAX_HEIGHT


        self.image = pygame.Surface((12, 12))
        self.image.fill(pygame.Color(255, 255, 255))

        self.rect = self.image.get_rect()

        if side:
            self.rect.x = self.ratio_padding_left*self.WIDTH
        else:
            self.rect.x = self.WIDTH*(1-self.ratio_padding_left)

        self.rect.centery = self.HEIGHT/2


    
    def move_back(self):
        if self.rect.centery > self.MIN_HEIGHT:
            self.rect.centery = self.MIN_HEIGHT
        if self.rect.centery < self.MAX_HEIGHT:
            self.rect.centery = self.MAX_HEIGHT



    def handle_input(self, key_dict, fps):
        if key_dict[pygame.K_z]:
            self.rect.y -= 1/fps*self.speed*self.MAX_HEIGHT
        elif key_dict[pygame.K_s]:
            self.rect.y += 1/fps*self.speed*self.MAX_HEIGHT

        if not (self.MIN_HEIGHT > self.rect.centery >= self.MAX_HEIGHT):
            self.move_back()


    def update(self, key_dict, fps, *_):
        self.handle_input(key_dict, fps)


class VerticalBar(pygame.sprite.Sprite):

    def __init__(self, side: bool = True) -> None:
        super().__init__()
        self.ratio_padding_left = 0.08

        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()

        self.image = pygame.image.load("asset/image/hud/vertical_bar.png")
        self.rect = self.image.get_rect()

        if side:
            self.rect.x = self.ratio_padding_left*self.WIDTH - 7
        else:
            self.rect.x = self.WIDTH*(1-self.ratio_padding_left) - 7

        self.rect.centery = self.HEIGHT/2