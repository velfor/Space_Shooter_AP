import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, image_dict, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image_dict = image_dict
        self.image = self.image_dict[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.frame_delay = 50
        self.anim_timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.anim_timer > self.frame_delay:
            self.anim_timer = now
            self.frame += 1
            if self.frame < 9:
                old_center = self.rect.center
                self.image = self.image_dict[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = old_center
            else:
                self.kill()