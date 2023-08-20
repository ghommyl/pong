import logging
import sys

import pygame

from settings import settings


class Game:
    def __init__(self):
        self.screen_width, self.screen_height = settings["screen_width"], settings["screen_height"]

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        pygame.display.set_caption("Welcome to Pong Game!")

        self.bg_color = tuple(settings["bg_color"])

        self.clock = pygame.time.Clock()

        self.fps = settings["fps"]

        self.paddle_width, self.paddle_height = settings["paddle_width"], settings["paddle_height"]
        self.paddle_border_distance_x = settings["paddle_border_distance_x"]
        self.paddle_left = Paddle(self.paddle_border_distance_x,                                            # left
                                  round(self.screen_height / 2 - self.paddle_height / 2),                   # top
                                  self.paddle_width, self.paddle_height)
        self.paddle_right = Paddle(self.screen_width - self.paddle_border_distance_x - self.paddle_width,   # left
                                   round(self.screen_height / 2 - self.paddle_height / 2),                  # top
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
                
                case pygame.KEYDOWN:
                    self._check_keydown_events(event)
                case pygame.KEYUP:
                    self._check_keyup_events(event)
    
    def _update_screen(self):
        self.paddle_left.update()
        self.paddle_right.update()

        self.screen.fill(self.bg_color)

        pygame.draw.rect(self.screen, settings["paddle_color"], self.paddle_left)
        pygame.draw.rect(self.screen, settings["paddle_color"], self.paddle_right)

        self.clock.tick(self.fps)
        pygame.display.flip()
    
    def _check_collisions(self):
        pass

    def _check_keydown_events(self, event):
        match event.key:
            case pygame.K_w:
                logging.debug("left paddle moving up")
                self.paddle_left.moving_up = True
            case pygame.K_s:
                logging.debug("left paddle moving down")
                self.paddle_left.moving_down = True
            case pygame.K_UP:
                logging.debug("right paddle moving up")
                self.paddle_right.moving_up = True
            case pygame.K_DOWN:
                logging.debug("right paddle moving down")
                self.paddle_right.moving_down = True
            
            case pygame.K_q:
                logging.info("exiting game")
                sys.exit()

    def _check_keyup_events(self, event):
        match event.key:
            case pygame.K_w:
                logging.debug("left paddle stopped")
                self.paddle_left.moving_up = False
            case pygame.K_s:
                logging.debug("left paddle stopped")
                self.paddle_left.moving_down = False
            case pygame.K_UP:
                logging.debug("right paddle stopped")
                self.paddle_right.moving_up = False
            case pygame.K_DOWN:
                logging.debug("right paddle stopped")
                self.paddle_right.moving_down = False


class Paddle(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
        self.moving_up = self.moving_down = False
        self.speed = settings["paddle_speed"]
        self.screen_width, self.screen_height = settings["screen_width"], settings["screen_height"]

    def update(self):
        if self.moving_up:
            self.top -= self.speed
        if self.moving_down:
            self.top += self.speed
        if self.top < 0:
            self.top = 0
        if self.bottom > self.screen_height:
            self.bottom = self.screen_height
