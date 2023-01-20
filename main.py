import pygame
from pygame.constants import QUIT
import random

pygame.init()

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

# create window
gameDisplay = pygame.display.set_mode(screen)

# set ball settings
ball = pygame.Surface((20, 20))
ball.fill((255, 255, 255))
ball_rect = ball.get_rect()
ball_speed = [1, 1]

# check for the quit
isWorking = True
while isWorking:
    for event in pygame.event.get():
        if event.type == QUIT:
            isWorking = False

    # refill display each iteration
    gameDisplay.fill((0, 0, 0))

    # set movement of the ball
    ball_rect = ball_rect.move(ball_speed)

    # return the ball from the sides of the screen
    if ball_rect.bottom >= height or ball_rect.top <= 0:
        ball_speed[1] = -ball_speed[1]
        ball.fill(random.choice(colorList))
    if ball_rect.right >= width or ball_rect.left <= 0:
        ball_speed[0] = -ball_speed[0]
        ball.fill(random.choice(colorList))
    
    # draw ball on the display
    gameDisplay.blit(ball, ball_rect)
    
    # update screen
    pygame.display.flip()