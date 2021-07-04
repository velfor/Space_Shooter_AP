import pygame
import random
from const import *

class Bonus(pygame.sprite.Sprite):
    def __init__(self, image_dict, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['hp', 'gun', 'shield', 'score', 'bomb'])
        if self.type == 'bomb':
            bomb_img = image_dict[self.type]
            self.image = pygame.transform.scale(bomb_img, (50, 40))
            #self.image.set_colorkey(WHITE)
        else:
            self.image = image_dict[self.type]
            self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()