
import pygame

class Screen():

    def __init__(self) -> None:
        rate = 3/4
        self.window: pygame.Surface = pygame.display.set_mode((1920*rate, 1080*rate))
        print(f"diplaying a {self.window.get_rect().width}x{self.window.get_rect().height}")
        pygame.display.set_caption("Controller")
