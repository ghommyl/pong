import logging
import sys

import pygame

from settings import settings

logging.basicConfig(level=logging.DEBUG, format="%(levelname)-10s- %(message)s")


class Game:
    def __init__(self):
        self.screen_width, self.screen_height = settings["screen_width"], settings["screen_height"]
        logging.info(f"screen width: {self.screen_width}, screen height: {self.screen_height}")

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        pygame.display.set_caption("Welcome to Pong Game!")

        self.bg_color = tuple(settings["bg_color"])
        logging.info(f"bg_color: {self.bg_color}")

        self.clock = pygame.time.Clock()

        self.fps = settings["fps"]
        logging.info(f"fps: {self.fps}")

        self.paddle_width, self.paddle_height = settings["paddle_width"], settings["paddle_height"]
        self.paddle_border_distance_x = settings["paddle_border_distance_x"]
        self.paddle_left_rect = pygame.Rect(self.paddle_border_distance_x, 
                                       round(self.screen_height / 2 - self.paddle_height / 2), 
                                       self.paddle_width, self.paddle_height)
        self.paddle_right_rect = pygame.Rect(self.screen_width - self.paddle_border_distance_x - self.paddle_width, 
                                        round(self.screen_height / 2 - self.paddle_height / 2), 
                                        self.paddle_width, self.paddle_height)
    
    def run(self):
        while True:
            self._check_events()
            self._check_collisions()
            self._update_screen()
    
    def _check_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    logging.info("exiting game")
                    sys.exit()
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)

        # blit something on the screen
        pygame.draw.rect(self.screen, settings["paddle_color"], self.paddle_left_rect)
        pygame.draw.rect(self.screen, settings["paddle_color"], self.paddle_right_rect)

        self.clock.tick(self.fps)
        pygame.display.flip()
    
    def _check_collisions(self):
        pass
