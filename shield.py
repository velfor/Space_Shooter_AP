import pygame
from const import *
import random

class Shield(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        #pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("PNG\\Effects\\shield1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.hide = True
        self.radius = self.rect.width // 2

    def update(self, center):
        if self.hide:
            self.rect.center = (-100, -100)
        else:
            self.rect.center = center
        now = pygame.time.get_ticks()
        if now - self.last_update > 5000:
            self.last_update = now
            self.hide = True


