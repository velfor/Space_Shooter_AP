import pygame
from const import *
import random


class Meteor(pygame.sprite.Sprite):
    def __init__(self, image_list):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((40, 40))
        #self.image.fill(BROWN)

        self.image_original = random.choice(image_list)
        self.image_original.set_colorkey(BLACK)
        self.image = self.image_original.copy()

        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.8 / 2
        self.rect.bottom = random.randint(-80, 0)
        self.rect.left = random.randint(0, SCREEN_WIDTH - 40)
        self.speedx = random.randint(-2, 2)
        self.speedy = random.randint(1, 5)
        self.angle = 0
        self.rotate_speed = random.randint(-8, 8)
        self.rotate_timer = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #self.image = pygame.transform.rotate(self.image, self.rotate_speed)
        now = pygame.time.get_ticks()
        # если с последнего вращения прошло > 50 мс
        if now - self.rotate_timer > 50:
            # вращаем
            self.rotate_timer = now
            self.angle = (self.angle + self.rotate_speed) % 360
            new_image = pygame.transform.rotate(self.image_original, self.angle)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = random.randint(-80, 0)
            self.rect.left = random.randint(0, SCREEN_WIDTH - 40)
            self.speedx = random.randint(-2, 2)
            self.speedy = random.randint(1, 5)

