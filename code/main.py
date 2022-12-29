import pygame
import sys
from game_data import level_1
from level import Level

from settings import *

pygame.init()
FPS = 60
screen = pygame.display.set_mode((w, h))
BLACK = pygame.Color('black')
clock = pygame.time.Clock()
level = Level(level_1, screen)
run = True
while run:
    screen.fill(BLACK)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    level.run(screen)
    pygame.display.flip()
pygame.quit()
