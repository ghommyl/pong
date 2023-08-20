import logging
import sys

import pygame

from settings import settings

logging.basicConfig(level=logging.DEBUG, format="%(levelname)-10s- %(message)s")


class Game:
    def __init__(self):
        self.screen_width, self.screen_height = settings["screen_width"], settings["screen_height"]
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        logging.info(f"screen width: {self.screen_width}, screen height: {self.screen_height}")
        pygame.display.set_caption("Welcome to Pong Game!")
        self.bg_color = tuple(settings["bg_color"])
        logging.info(f"bg_color: {self.bg_color}")
        self.clock = pygame.time.Clock()
        self.fps = settings["fps"]
        logging.info(f"fps: {self.fps}")
    
    def run(self):
        while True:
            self._check_events()

            # check collisions

            self._udpate_screen()
    
    def _check_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    logging.info("exiting game")
                    sys.exit()
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)

        # blit something on the screen

        self.clock.tick(self.fps)
        pygame.display.flip()
