import pygame
import sys
from game_data import level_1, level_2
from level import Level

from settings import *

pygame.init()
FPS = 60
screen = pygame.display.set_mode((w, h))
BLACK = pygame.Color('black')
clock = pygame.time.Clock()
level = Level(level_1, level_2, screen)
run = True
while run:
    screen.fill('green')
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    level.run()
    pygame.display.flip()
pygame.quit()