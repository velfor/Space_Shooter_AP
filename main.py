import pygame
import sys
import random
from const import *
from ship import Ship
from meteor import Meteor
from bullet import Bullet
from explosion import Explosion
from bonus import Bonus
from shield import Shield

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Shooter')
#pygame.display.set_icon(pygame.image.load('logo.png'))
clock = pygame.time.Clock()
# создаем группы
all_sprites = pygame.sprite.Group()
meteors = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
# создаем игровые объекты

background_img = pygame.image.load('Backgrounds\\black.png').convert()
background = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_rect = background.get_rect()

player = Ship()

meteor_filename_list = ['meteorGrey_big1.png', 'meteorGrey_big2.png', 'meteorGrey_med1.png', 'meteorGrey_med2.png',
                     'meteorGrey_small1.png', 'meteorGrey_small2.png', 'meteorGrey_tiny1.png', 'meteorGrey_tiny2.png',
                        'meteorGrey_big3.png', 'meteorGrey_big4.png']

meteor_image_list = []
for filename in meteor_filename_list:
    meteor_image = pygame.image.load('PNG\\Meteors\\' + filename).convert()
    meteor_image_list.append(meteor_image)

explosion_image_dict = {}
explosion_image_dict['small'] = []
explosion_image_dict['large'] = []
for i in range(9):
    file_name = f'regularExplosion0{i}.png' #'regularExplosion0' + str(i) + '.png'
    explosion_image = pygame.image.load('PNG\\'+file_name).convert()
    explosion_image.set_colorkey(BLACK)
    large_image = pygame.transform.scale(explosion_image, (80, 80))
    explosion_image_dict['large'].append(large_image)
    #med

    #small
    small_image = pygame.transform.scale(explosion_image, (20, 20))
    explosion_image_dict['small'].append(small_image)
    #tiny

#словарь изображений для бонусов
bonus_image_dict = {}
bonus_image_dict['hp'] = pygame.image.load('PNG\\Power-ups\\' + 'pill_green.png').convert()
bonus_image_dict['gun'] = pygame.image.load('PNG\\Power-ups\\' + 'bolt_gold.png').convert()
bonus_image_dict['shield'] = pygame.image.load('PNG\\Power-ups\\' + 'shield_gold.png').convert()
bonus_image_dict['score'] = pygame.image.load('PNG\\Power-ups\\' + 'star_gold.png').convert()
bonus_image_dict['bomb'] = pygame.image.load('PNG\\' + 'bomb.png').convert_alpha()


#=====ФУНКЦИИ=====
def create_meteor(meteor_image_list):
    meteor = Meteor(meteor_image_list)
    all_sprites.add(meteor)
    meteors.add(meteor)

def draw_hp_bar():
    if player.hp < 0:
        player.hp = 0
    fill = (player.hp / 100) * HP_BAR_WIDTH
    outline_rect = pygame.Rect(SCREEN_WIDTH - HP_BAR_WIDTH - 10, 10, HP_BAR_WIDTH, HP_BAR_HEIGHT)
    fill_rect = pygame.Rect(SCREEN_WIDTH - HP_BAR_WIDTH - 10, 10, fill, HP_BAR_HEIGHT)
    pygame.draw.rect(screen, GREEN, fill_rect)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)

def draw_text(surf, text, size, x, y,):
    font = pygame.font.SysFont('arial', size)
    text_surface = font.render(text, True, YELLOW)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def intro():
    screen.blit(background, background_rect)
    draw_text(screen, "Space Shooter", 48, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    pygame.display.flip()
    wait = True
    while wait:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP:
                wait = False


#=====КОНЕЦ ФУНКЦИЙ======


for i in range(METEORS_QTY):
    create_meteor(meteor_image_list)
# добавляем объекты в группы
all_sprites.add(player)
# переменные
score = 0
#shield = None
shield = Shield((-100, -100))

intro()
while True:
    clock.tick(FPS)
    #обработка ввода
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # кнопка мыши нажата и эта кнопка левая
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if player.gun_bonus:
                #3 пули
                bullet1 = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet1)
                bullets.add(bullet1)

                bullet2 = Bullet(player.rect.left, player.rect.centery)
                all_sprites.add(bullet2)
                bullets.add(bullet2)

                bullet3 = Bullet(player.rect.right, player.rect.centery)
                all_sprites.add(bullet3)
                bullets.add(bullet3)

            else:
                #1 пуля
                bullet = Bullet(player.rect.centerx, player.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    #update and collisions
    all_sprites.update()
    if shield != None:
        shield.update(player.rect.center)


    #игрок с метеорами
    player_hits_meteors = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
    for hit in player_hits_meteors:
        #метеорит отнимает hp у игрока
        #big
        if hit.radius >= 35:
            player.hp -= 50
        elif hit.radius < 35 and hit.radius >= 17:
            player.hp -= 25
        elif hit.radius < 17 and hit.radius >= 11:
            player.hp -= 10
        else:
            player.hp -= 5
        if player.hp <= 0:
            pygame.quit()
            sys.exit()
        create_meteor(meteor_image_list)
    # щит с метеорами
    shield_hits_meteors = pygame.sprite.spritecollide(shield, meteors, True, pygame.sprite.collide_circle)
    for hit in shield_hits_meteors:
        create_meteor(meteor_image_list)

    #пули с метеорами
    bullets_hits_meteors = pygame.sprite.groupcollide(meteors, bullets, True, True)
    for hit in bullets_hits_meteors:
        # начисление очков
        if hit.radius >= 35:
            score += 5
        elif hit.radius < 35 and hit.radius >= 17:
            score += 10
        elif hit.radius < 17 and hit.radius >= 11:
            score += 20
        else:
            score += 40
        # шанс выпадения бонуса 1 из 10
        if random.random() > 0.5:
            #показываем бонус
            bonus = Bonus(bonus_image_dict, hit.rect.center)
            bonuses.add(bonus)
            all_sprites.add(bonus)
        else:

            # показ взрыва
            # big meteor
            if hit.radius >= 35:
                explosion = Explosion(explosion_image_dict, hit.rect.center, 'large')
                all_sprites.add(explosion)
            # medium meteor
            # small meteor
            elif hit.radius < 17 and hit.radius >= 11:
                explosion = Explosion(explosion_image_dict, hit.rect.center, 'small')
                all_sprites.add(explosion)
            # tiny meteor
            # новый метеор вместо сбитого
        create_meteor(meteor_image_list)
    #проверка что бонус подобран игроком
    player_hits_bonuses = pygame.sprite.spritecollide(player, bonuses, True, pygame.sprite.collide_circle)
    for hit in player_hits_bonuses:
        if hit.type == 'hp':
            player.hp += random.randint(20, 50)
            if player.hp > 100:
                player.hp = 100
        elif hit.type == 'gun':
            player.gun_bonus = True
            player.gun_bonus_timer = pygame.time.get_ticks()
        elif hit.type == 'shield':
            shield = Shield(player.rect.center)
            shield.hide = False
            #shield.last_update = pygame.time.get_ticks()
        elif hit.type == 'score':
            pass
        elif hit.type == 'bomb':
            player.hp = 5
    #draw
    #screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    #рисуем полоску hp
    draw_hp_bar()
    #рисуем щит
    if shield != None:
        screen.blit(shield.image, shield.rect)
    pygame.display.flip()