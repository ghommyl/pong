import logging
import sys

import pygame

from settings import settings
from sprites import Paddle, Ball
from text import Score, Text


class Game:
    def __init__(self):
        pygame.init()

        self.screen_width, self.screen_height = settings["screen_width"], settings["screen_height"]

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.screen_rect = self.screen.get_rect()
        
        pygame.display.set_caption("Welcome to Pong Game!")

        self.bg_color = tuple(settings["bg_color"])

        self.clock = pygame.time.Clock()

        self.fps = settings["fps"]

        self.paddle_width, self.paddle_height = settings["paddle_width"], settings["paddle_height"]
        self.paddle_border_distance_x = settings["paddle_border_distance_x"]
        self.paddle_left = Paddle(self.paddle_border_distance_x,                                            # left
                                  self.screen_height / 2 - self.paddle_height / 2,                          # top
                                  self.paddle_width, self.paddle_height)
        self.paddle_right = Paddle(self.screen_width - self.paddle_border_distance_x - self.paddle_width,   # left
                                   self.screen_height / 2 - self.paddle_height / 2,                         # top
                                   self.paddle_width, self.paddle_height)
        
        self.score = Score(self.screen)

        self.ball_radius = settings["ball_radius"]
        self.ball = Ball(self.ball_radius, self.paddle_left, self.paddle_right, self.score)

        self.paused = False
        self.paused_text = Text("Paused", self.screen)
        self.paused_text.prep_rect()
        self.paused_text.rect.center = self.screen_rect.center
    
    def run(self):
        while True:
            self._check_events()
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
        self.screen.fill(self.bg_color)

        if self.paused:
            self.paused_text.draw()
            logging.debug("Paused text blitted")

        else:
            self.paddle_left.update()
            self.paddle_right.update()
            self.ball.update()

        self.score.draw()

        pygame.draw.rect(self.screen, self.paddle_left.color, self.paddle_left)
        pygame.draw.rect(self.screen, self.paddle_right.color, self.paddle_right)
        pygame.draw.circle(self.screen, self.ball.color,
                        (self.ball.x, self.ball.y), self.ball.radius)

        self.clock.tick(self.fps)
        pygame.display.flip()

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

            case pygame.K_SPACE:
                logging.info("game paused/continued")
                self.paused = not self.paused

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
