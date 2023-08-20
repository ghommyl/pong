import logging

import pygame

from settings import settings

logging.basicConfig(level=logging.DEBUG, format="%(levelname)-10s- %(message)s")


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((settings["screen_width"], settings["screen_height"]))
        pygame.display.set_caption("Welcome to Pong Game!")
        self.bg_color = tuple(settings["bg_color"])
        self.clock = pygame.time.Clock()
        self.fps = settings["fps"]
        logging.info(f"fps: {self.fps}")
    
    def run(self):
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        logging.info("quitting game")
                        return

            self.screen.fill(self.bg_color)

            # blit something on the screen

            self.clock.tick(self.fps)
            pygame.display.flip()
