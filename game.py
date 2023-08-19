import logging

import pygame

from colors import *


class Game:
    def __init__(self, screen_width=1200, screen_height=800):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Welcome to Pong Game!")
        self.bg_color = BLACK
        self.clock = pygame.time.Clock()
        self.fps = 60
    
    def run(self):
        keep_going = True
        while keep_going:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        logging.info("Game quit")
                        keep_going = False

            self.screen.fill(self.bg_color)

            # blit something on the screen

            self.clock.tick(self.fps)
            pygame.display.flip()
