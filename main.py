import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

import random

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

colorList = [GREEN, BLUE, RED, YELLOW, PURPLE, CYAN]

font = pygame.font.SysFont('Verdana', 20)

# create window
gameDisplay = pygame.display.set_mode(screen)

# set ball settings
ball = pygame.Surface((20, 20))
ball.fill(WHITE)
ball_rect = ball.get_rect()
ball_speed = 5

# create instance of enemy
def create_enemy():
    enemy = pygame.Surface((20, 20))
    enemy.fill(RED)
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(1, 5)

    return [enemy, enemy_rect, enemy_speed]

CREATE_ENEMY = pygame.USEREVENT + 1 #why + 1?
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

# create instance of bonus
def create_bonus():
    bonus = pygame.Surface((20, 20))
    bonus.fill(GREEN)
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(1, 5)

    return [bonus, bonus_rect, bonus_speed]

CREATE_BONUS = pygame.USEREVENT
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

    # refill display each iteration
    gameDisplay.fill(BLACK)

    # # set movement of the ball
    # ball_rect = ball_rect.move(ball_speed)

    # # return the ball from the sides of the screen
    # if ball_rect.bottom >= height or ball_rect.top <= 0:
    #     ball_speed[1] = -ball_speed[1]
    #     ball.fill(random.choice(colorList))
    # if ball_rect.right >= width or ball_rect.left <= 0:
    #     ball_speed[0] = -ball_speed[0]
    #     ball.fill(random.choice(colorList))

    pressed_keys = pygame.key.get_pressed()
    
    # draw ball on the display
    gameDisplay.blit(ball, ball_rect)

    gameDisplay.blit(font.render("SCORE: " + str(score), True, WHITE), (width - 150, 0))


    # set behavior of enemies
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2],0)
        gameDisplay.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            isWorking = False

    # set behavior of bonuses
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        gameDisplay.blit(bonus[0], bonus[1])

        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))

        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    # set movement of the ball
    if pressed_keys[K_DOWN] and ball_rect.bottom <= height:
        ball_rect = ball_rect.move((0, ball_speed))
    if pressed_keys[K_UP] and ball_rect.top >= 0:
        ball_rect = ball_rect.move((0, -ball_speed))
    if pressed_keys[K_RIGHT] and ball_rect.right <= width:
        ball_rect = ball_rect.move((ball_speed, 0))
    if pressed_keys[K_LEFT] and ball_rect.left >= 0:
        ball_rect = ball_rect.move((-ball_speed, 0))

    #  print(len(enemies))

    # update screen
    pygame.display.flip()