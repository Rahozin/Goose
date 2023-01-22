import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

import random
from os import listdir

pygame.init()

FPS = pygame.time.Clock()

# set screen size
screen = width, height = 800, 600


# colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
PURPLE = 255, 0, 255
CYAN = 0, 255, 255
DARKGRAY = 20, 20, 20

colorList = [GREEN, BLUE, RED, YELLOW, PURPLE, CYAN]

font = pygame.font.SysFont('Verdana', 20)


# create window
gameDisplay = pygame.display.set_mode(screen)


# make background moving
bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3


# set player`s animation and settings
ANIMATION_GOOSE_PATH = 'animation_goose'
player_imgs = [pygame.transform.scale(pygame.image.load(ANIMATION_GOOSE_PATH + '/' + img).convert_alpha(), (120, 50)) for img in listdir(ANIMATION_GOOSE_PATH)]
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 5

CHANGE_IMG = pygame.USEREVENT + 0
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0


# create instance of enemy
def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (100, 25))
    enemy_rect = pygame.Rect(width, random.randint(0.05*height, 0.95*height), *enemy.get_size())
    enemy_speed = random.randint(1, 5)

    return [enemy, enemy_rect, enemy_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []


# create instance of bonus
def create_bonus():
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (40, 60))
    bonus_rect = pygame.Rect(random.randint(0.05*width, 0.95*width), 0, *bonus.get_size())
    bonus_speed = random.randint(1, 5)

    return [bonus, bonus_rect, bonus_speed]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)

bonuses = []

score = 0


# check for the quit and othe events
isWorking = True
while isWorking:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            isWorking = False
        
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        
        # change player`s image
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]


    # scan if keys was pressed
    pressed_keys = pygame.key.get_pressed()
    

    # draw all objects each iteration
    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX <= -bg.get_width():
        bgX = bg.get_width()
    
    if bgX2 <= -bg.get_width():
        bgX2 = bg.get_width()

    gameDisplay.blit(bg, (bgX, 0))
    gameDisplay.blit(bg, (bgX2, 0))

    gameDisplay.blit(player, player_rect)

    gameDisplay.blit(font.render("SCORE: " + str(score), True, DARKGRAY), (width - 150, 0))


    # set behavior of enemies
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2],0)
        gameDisplay.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            isWorking = False


    # set behavior of bonuses
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        gameDisplay.blit(bonus[0], bonus[1])

        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1


    # set movement of the player
    if pressed_keys[K_DOWN] and player_rect.bottom <= height:
        player_rect = player_rect.move((0, player_speed))
    if pressed_keys[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move((0, -player_speed))
    if pressed_keys[K_RIGHT] and player_rect.right <= width:
        player_rect = player_rect.move((player_speed, 0))
    if pressed_keys[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move((-player_speed, 0))


    # update screen
    pygame.display.flip()