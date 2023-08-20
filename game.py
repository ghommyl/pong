import logging
import math
import random
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
                                  self.screen_height / 2 - self.paddle_height / 2,                          # top
                                  self.paddle_width, self.paddle_height)
        self.paddle_right = Paddle(self.screen_width - self.paddle_border_distance_x - self.paddle_width,   # left
                                   self.screen_height / 2 - self.paddle_height / 2,                         # top
                                   self.paddle_width, self.paddle_height)
        
        self.ball_radius = settings["ball_radius"]
        self.ball = Ball(self.ball_radius, self.paddle_left, self.paddle_right)
    
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
        self.paddle_left.update()
        self.paddle_right.update()
        self.ball.update()

        self.screen.fill(self.bg_color)

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
        self.color = tuple(settings["paddle_color"])

    def update(self):
        if self.moving_up:
            self.top -= self.speed
        if self.moving_down:
            self.top += self.speed
        if self.top < 0:
            self.top = 0
        if self.bottom > self.screen_height:
            self.bottom = self.screen_height


class Ball:
    def __init__(self, radius, paddle_left, paddle_right):
        self.screen_width, self.screen_height = settings["screen_width"], settings["screen_height"]
        self.x, self.y = self.screen_width / 2, self.screen_height / 2
        self.radius = radius
        self.color = settings["ball_color"]
        self.angles = [math.pi / (180 / settings["ball_angle"]),
                       math.pi / (180 / (360 - settings["ball_angle"])),
                       math.pi / (180 / (180 + settings["ball_angle"])),
                       math.pi / (180 / (180 - settings["ball_angle"]))]
        self.angle = math.pi / (180 / random.choice([settings["ball_angle"],
                                                     360 - settings["ball_angle"],
                                                     180 + settings["ball_angle"],
                                                     180 - settings["ball_angle"]]))
        self.speed = settings["ball_speed"]
        
        self.paddle_left, self.paddle_right = paddle_left, paddle_right
    
    def update(self):
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        self.x += dx
        self.y += dy
        self._check_collisions()
        winner = self._check_winner()
        if winner != 0:
            self.__init__(self.radius, self.paddle_left, self.paddle_right)
    
    def _check_collisions(self):
        if self.x <= self.paddle_left.right and self.paddle_left.top <= self.y <= self.paddle_left.bottom:
            if self.angle == self.angles[2]:
                logging.debug("angle from: 2, to: 1")
                self.angle = self.angles[1]

            elif self.angle == self.angles[3]:
                logging.debug("angle from: 3, to: 0")
                self.angle = self.angles[0]

        elif self.x >= self.paddle_right.left and self.paddle_right.top <= self.y <= self.paddle_right.bottom:
            if self.angle == self.angles[0]:
                logging.debug("angle from: 0, to: 3")
                self.angle = self.angles[3]
            
            elif self.angle == self.angles[1]:
                logging.debug("angle from: 1, to: 2")
                self.angle = self.angles[2]

        if self.y <= 0:
            if self.angle == self.angles[1]:
                logging.debug("angle from: 1, to: 0")
                self.angle = self.angles[0]
            
            elif self.angle == self.angles[2]:
                logging.debug("angle from: 2, to: 3")
                self.angle = self.angles[3]
        
        elif self.y >= self.screen_height:
            if self.angle == self.angles[0]:
                logging.debug("angle from: 0, to: 1")
                self.angle = self.angles[1]

            elif self.angle == self.angles[3]:
                logging.debug("angle from: 3, to: 2")
                self.angle = self.angles[2]
    
    def _check_winner(self):
        if self.x <= 0:
            return 1
        elif self.x >= self.screen_width:
            return -1
        return 0
