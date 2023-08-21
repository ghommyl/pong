import logging
import math
import random

import pygame

from settings import settings


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
    def __init__(self, radius, paddle_left, paddle_right, score):
        self.screen_width, self.screen_height = settings["screen_width"], settings["screen_height"]
        self.x, self.y = self.screen_width / 2, random.uniform(0, self.screen_height)
        self.radius = radius
        self.color = settings["ball_color"]

        self.ball_angle = random.uniform(30, 60)
        logging.info(f"ball_angle: {self.ball_angle}")
        self.angles = [math.pi / (180 / self.ball_angle),
                       math.pi / (180 / (360 - self.ball_angle)),
                       math.pi / (180 / (180 + self.ball_angle)),
                       math.pi / (180 / (180 - self.ball_angle))]
        self.angle = random.choice(self.angles)
        
        self.speed = random.uniform(7, 10)
        logging.info(f"ball_speed: {self.speed}")
        
        self.paddle_left, self.paddle_right = paddle_left, paddle_right
        
        self.score = score

        self.removed = False
    
    def update(self):
        dx = math.cos(self.angle) * self.speed
        dy = math.sin(self.angle) * self.speed
        self.x += dx
        self.y += dy
        self._check_collisions()
        winner = self._check_winner()
        if winner != 0:
            if winner == -1:
                self.score.left += 1
            elif winner == 1:
                self.score.right += 1
            self.removed = True
    
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
