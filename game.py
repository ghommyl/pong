import logging
import math
import random
import sys

import pygame

from settings import settings


class Game:
    def __init__(self):
        pygame.init()

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
        
        self.score = Score(self.screen)

        self.ball_radius = settings["ball_radius"]
        self.ball = Ball(self.ball_radius, self.paddle_left, self.paddle_right, self.score)

        self.paused = False
    
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
        if not self.paused:
            self.paddle_left.update()
            self.paddle_right.update()
            self.ball.update()

            self.screen.fill(self.bg_color)

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
        self.x, self.y = self.screen_width / 2, self.screen_height / 2
        self.radius = radius
        self.color = settings["ball_color"]

        self.angles = [math.pi / (180 / settings["ball_angle"]),
                       math.pi / (180 / (360 - settings["ball_angle"])),
                       math.pi / (180 / (180 + settings["ball_angle"])),
                       math.pi / (180 / (180 - settings["ball_angle"]))]
        self.angle = random.choice(self.angles)
        
        self.speed = settings["ball_speed"]
        
        self.paddle_left, self.paddle_right = paddle_left, paddle_right
        
        self.score = score
    
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
            self.__init__(self.radius, self.paddle_left, self.paddle_right, self.score)
    
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


class Score:
    def __init__(self, screen):
        self.left = self.right = 0
        self.font = pygame.font.SysFont("monospace", 40)
        self.screen_width = settings["screen_width"]
        self.score_midx_distance = settings["score_midx_distance"]
        self.score_border_distance_y = settings["score_border_distance_y"]
        self.screen = screen
        self.text_color = settings["text_color"]
        self.bg_color = settings["bg_color"]
    
    def draw(self):
        for i, n in (-1, self.left), (1, self.right):
            text = str(n)
            img = self.font.render(text, True, self.text_color, self.bg_color)
            rect = img.get_rect()
            rect.top = self.score_border_distance_y
            if i == -1:
                rect.right = self.screen_width / 2 - self.score_midx_distance
            elif i == 1:
                rect.left = self.screen_width / 2 + self.score_midx_distance
            self.screen.blit(img, rect)
