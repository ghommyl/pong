import random
import sys

import pygame

from settings import settings
from sprites import Paddle, Ball
from text import Score, Text


class Game:
    def __init__(self, logger):
        pygame.init()

        self.logger = logger

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
        self.ball_group = set([Ball(self.logger, self.ball_radius, self.paddle_left, self.paddle_right, self.score)])
        self.ball_appear_dt = settings["ball_appear_dt"]

        self.paused = False
        self.paused_text = Text("Paused", self.screen)
        self.paused_text.prep_rect()
        self.paused_text.rect.center = self.screen_rect.center
    
    def run(self):
        time = 0
        while True:
            time += 1
            self._check_events(time)
            self._update_screen()
            if time == self.ball_appear_dt:
                time = 0
    
    def _check_events(self, time):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.logger.info("exiting game")
                    sys.exit()
                
                case pygame.KEYDOWN:
                    self._check_keydown_events(event)
                case pygame.KEYUP:
                    self._check_keyup_events(event)
        
        if time % self.ball_appear_dt == 0 and random.randint(0, 1):
            self.ball_group.add(Ball(self.logger, self.ball_radius, self.paddle_left, self.paddle_right, self.score))
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)

        if self.paused:
            self.paused_text.draw()
            self.logger.debug("Paused text blitted")

        else:
            self.paddle_left.update()
            self.paddle_right.update()
            for ball in self.ball_group.copy():
                ball.update()
                if ball.removed:
                    self.ball_group.remove(ball)

        self.score.draw()

        pygame.draw.rect(self.screen, self.paddle_left.color, self.paddle_left)
        pygame.draw.rect(self.screen, self.paddle_right.color, self.paddle_right)
        for ball in self.ball_group:
            pygame.draw.circle(self.screen, ball.color,
                               (ball.x, ball.y), ball.radius)

        self.clock.tick(self.fps)
        pygame.display.flip()

    def _check_keydown_events(self, event):
        match event.key:
            case pygame.K_w:
                self.logger.debug("left paddle moving up")
                self.paddle_left.moving_up = True
            case pygame.K_s:
                self.logger.debug("left paddle moving down")
                self.paddle_left.moving_down = True
            case pygame.K_UP:
                self.logger.debug("right paddle moving up")
                self.paddle_right.moving_up = True
            case pygame.K_DOWN:
                self.logger.debug("right paddle moving down")
                self.paddle_right.moving_down = True
            
            case pygame.K_q:
                self.logger.info("exiting game")
                sys.exit()

            case pygame.K_SPACE:
                self.logger.info("game paused/continued")
                self.paused = not self.paused

    def _check_keyup_events(self, event):
        match event.key:
            case pygame.K_w:
                self.logger.debug("left paddle stopped")
                self.paddle_left.moving_up = False
            case pygame.K_s:
                self.logger.debug("left paddle stopped")
                self.paddle_left.moving_down = False
            case pygame.K_UP:
                self.logger.debug("right paddle stopped")
                self.paddle_right.moving_up = False
            case pygame.K_DOWN:
                self.logger.debug("right paddle stopped")
                self.paddle_right.moving_down = False
