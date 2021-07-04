import pygame
from const import *


class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((50, 50))
        #self.image.fill(GREEN)
        self.image = pygame.image.load('PNG/playerShip1_orange.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * 0.8 / 2
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speedx = 0
        self.hp = 100
        self.gun_bonus = False
        self.gun_bonus_timer = pygame.time.get_ticks()


    def update(self):
        self.speedx = 0
        key_state = pygame.key.get_pressed()
        if key_state[pygame.K_RIGHT] or key_state[pygame.K_d]:
            self.speedx = 10
        elif key_state[pygame.K_LEFT] or key_state[pygame.K_a]:
            self.speedx = -10
        self.rect.x += self.speedx
        # контроль границ
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        # проверяем что истекло время бонуса пушки
        now = pygame.time.get_ticks()
        if self.gun_bonus and now - self.gun_bonus_timer > 5000:
            self.gun_bonus_timer = now
            self.gun_bonus = False
