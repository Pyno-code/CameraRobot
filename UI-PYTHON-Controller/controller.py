import time
import pygame
from camera_control.camera import Camera
from graphics.angle_indicator import AngleIndicator
from graphics.crosshair import Crosshair
from graphics.gyroscope import Gyroscope
from graphics.height_indicator import HeightIndicator, VerticalBar
from graphics.numeric_indicator import NumericIndicator
from graphics.compass_indicator import CompassIndicator, PointerIndicator
from graphics.width_indicator import HorizontalBar, WidthIndicator




class Controller:

    def __init__(self, window: pygame.Surface, fps) -> None:

        self.WIDTH, self.HEIGHT = pygame.display.get_window_size()



        self.fps = fps
        self.group_hud_height_indicator = pygame.sprite.Group()
        self.group_hud_width_indicator = pygame.sprite.Group()
        self.group_hud_compass_indicator = pygame.sprite.Group()
        self.group_hud_crosshair = pygame.sprite.Group()
        self.group_hud_angle_bar = pygame.sprite.Group()
        self.group_hud_gyroscope = pygame.sprite.Group()

        self.height_indicator = HeightIndicator(True)
        self.group_hud_height_indicator.add(self.height_indicator,
                            HeightIndicator(False),
                            NumericIndicator(0.05*self.WIDTH, self.HEIGHT/2), 
                            VerticalBar(True),
                            VerticalBar(False))
        
        self.compass_indicator = CompassIndicator()
        self.group_hud_compass_indicator.add(self.compass_indicator,
                                            PointerIndicator(),
                                            PointerIndicator(False),
                                            NumericIndicator(self.WIDTH/2, self.HEIGHT*0.18))
        
        self.cross_hair = Crosshair()
        self.group_hud_crosshair.add(self.cross_hair,
                                    AngleIndicator(),
                                    AngleIndicator(False),
                                    NumericIndicator(self.WIDTH/2, self.HEIGHT/2))
        
        self.width_indicator = WidthIndicator()
        self.group_hud_width_indicator.add(HorizontalBar(),
                                        self.width_indicator,
                                        NumericIndicator(self.WIDTH/2, self.HEIGHT*(1-0.05)))
        
        self.group_hud_gyroscope.add(Gyroscope())

        self.cross_hair_active = False
        
        self.window = window
        
        self.stream = Camera(self.window)
        
        self.key_dict = {
            pygame.K_s: False, #descente
            pygame.K_z: False, #monter
            pygame.K_a: False, #rotation gauche
            pygame.K_e: False, #rotation droite
            pygame.K_q: False, #gauche
            pygame.K_d: False, #droite
            pygame.K_w: False, #rotation z bas
            pygame.K_c: False, #rotation z haut
            pygame.K_UP: False, #rotation x front
            pygame.K_DOWN: False, #rotation x back
            pygame.K_LEFT: False, #rotation y gauche
            pygame.K_RIGHT: False, #rotation y droite
        }
        

    def render(self):
        start = time.time()

        if self.stream.camera_alive:
            self.stream.frame()
            self.window.blit(self.stream.current_frame, (0, 0))
        else:
            self.window.fill((0, 0, 0))

        self.group_hud_height_indicator.draw(self.window)
        self.group_hud_compass_indicator.draw(self.window)
        self.group_hud_angle_bar.draw(self.window)
        self.group_hud_width_indicator.draw(self.window)
        self.group_hud_gyroscope.draw(self.window)


        if self.cross_hair_active:
            self.group_hud_crosshair.draw(self.window)

        # print("render time : ", time.time() - start)

        pygame.display.update()

    def handle_input(self):
        for event in pygame.event.get((pygame.KEYDOWN, pygame.KEYUP)):
                key_pressed = None
                if event.type == pygame.KEYUP:
                    key_pressed = False
                elif event.type == pygame.KEYDOWN:
                    key_pressed = True

                if key_pressed is not None and event.key in self.key_dict:
                    self.key_dict[event.key] = key_pressed

    def update(self):
        start = time.time()
        rate_height = int(-100*(self.height_indicator.rect.centery - self.height_indicator.MIN_HEIGHT)/abs(
            self.height_indicator.MAX_HEIGHT - self.height_indicator.MIN_HEIGHT))
        rate_width = int(-100*(self.width_indicator.rect.centerx - self.width_indicator.MIN_WIDTH)/abs(
            self.width_indicator.MAX_WIDTH - self.width_indicator.MIN_WIDTH))
        self.group_hud_height_indicator.update(self.key_dict, self.fps, rate_height)
        self.group_hud_width_indicator.update(self.key_dict, self.fps, rate_width)
        self.group_hud_compass_indicator.update(self.key_dict, self.fps, self.compass_indicator.angle)

        if self.cross_hair_active:
            self.group_hud_crosshair.update(self.key_dict, self.fps, self.cross_hair.angle)

        self.group_hud_gyroscope.update(self.key_dict, self.fps)
        # print("update time : ", time.time() - start)


