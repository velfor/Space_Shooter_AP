import pygame
from const import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, ship_x, ship_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = ship_x
        self.rect.bottom = ship_y
        self.speedy = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speedy
        if self.rect.top < 0:
            self.kill()
