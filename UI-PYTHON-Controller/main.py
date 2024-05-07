import time
import pygame
from controller import Controller
from screen import Screen
import os
from  timer_module.time_calcul import TimeCounter

class MainLoop:

    def __init__(self) -> None:
        pygame.init()
        self.screen = Screen()
        self.fps = 60
        self.controller = Controller(self.screen.window, self.fps)
        self.clock = pygame.time.Clock()
        self.running = True

        self.loop = TimeCounter(self.loop)

    def loop(self):
        start = time.time()
        self.controller.handle_input()
        self.controller.update()
        self.controller.render()
        # print("loop time : ", time.time() - start)

    def get_window_title(self):
        if self.loop.get_mean() != 0:
            fps = 1/self.loop.get_mean()
        else:
            fps = 0
        return f"fps : {fps}" 


    def start(self):
        while self.running:
            self.loop()
            self.clock.tick(self.fps)
            pygame.display.set_caption(self.get_window_title())
            for event in pygame.event.get(pygame.QUIT):
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()


if __name__ == "__main__":
    MainLoop().start()
    
