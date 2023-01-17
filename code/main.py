import pygame
import sys
from game_data import level_1, level_2
from start_window import StartWindow, End
from level import Level

from settings import *

pygame.init()
FPS = 60
screen = pygame.display.set_mode((w, h))
BLACK = pygame.Color('black')
clock = pygame.time.Clock()
level = Level(level_1, level_2, screen)


def terminate():
    pygame.quit()
    sys.exit()


def start_window():
    win = StartWindow(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if win.check_pressed(event.pos):
                        return
        win.run()
        pygame.display.flip()
        clock.tick(FPS)


def end_window():
    win = End(screen)
    screen.fill('black')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        win.run()
        pygame.display.flip()
        clock.tick(FPS)


run = True
start_window()
while run:
    screen.fill('black')
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            level.get_keys(event.button)
    level.run()
    if level.end_game():
        end_window()
    pygame.display.flip()
pygame.quit()