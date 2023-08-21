import pygame

from settings import settings


class Score:
    def __init__(self, screen):
        self.left = self.right = 0
        self.screen_width = settings["screen_width"]
        self.score_midx_distance = settings["score_midx_distance"]
        self.score_border_distance_y = settings["score_border_distance_y"]
        self.screen = screen
    
    def draw(self):
        for i, n in (-1, self.left), (1, self.right):
            text = Text(str(n), self.screen)
            text.prep_rect()
            text.rect.top = self.score_border_distance_y
            match i:
                case -1:
                    text.rect.right = self.screen_width / 2 - self.score_midx_distance
                case 1:
                    text.rect.left = self.screen_width / 2 + self.score_midx_distance
            text.draw()


class Text:
    def __init__(self, text, screen):
        self.text = text
        self.font = pygame.font.SysFont("monospace", 40)
        self.text_color = settings["text_color"]
        self.bg_color = settings["bg_color"]
        self.screen = screen
    
    def prep_rect(self):
        self.img = self.font.render(self.text, True, self.text_color, self.bg_color)
        self.rect = self.img.get_rect()
    
    def draw(self):
        self.screen.blit(self.img, self.rect)
