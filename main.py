import pygame
import sys
import os
from random import random


class Board:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                lt = (self.left + x * self.cell_size, self.top + y * self.cell_size)
                size = (self.cell_size, self.cell_size)
                pygame.draw.rect(screen, WHITE, (lt, size), 1)

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if self.left <= x <= self.left + self.width * self.cell_size and \
                self.top <= y <= self.top + self.height * self.cell_size:
            cell_x = (x - self.left) // self.cell_size
            cell_y = (y - self.top) // self.cell_size
            return cell_x, cell_y
        else:
            return None

    def on_click(self, cell_coords):
        if cell_coords:
            x, y = cell_coords
            self.board[y][x] = (self.board[y][x] + 1) % 3

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell_coords(self, cell_x, cell_y):
        x = self.left + cell_x * self.cell_size
        y = self.top + cell_y * self.cell_size
        return x, y


class Tree(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, ores)
        self.branches = ra






class Hero(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = load_image('Hero.png')
        self.rect = self.image.get_rect()
        self.dx = 50
        self.dy = 50
        x, y = board.get_cell_coords(pos_x, pos_y)
        self.rect.x = x
        self.rect.y = y

    def update_by_mouse(self, mouse_pos):
        cell_x, cell_y = board.get_cell(mouse_pos)
        x, y = board.get_cell_coords(cell_x, cell_y)
        self.rect.x = x
        self.rect.y = y

    def update_by_keyboard(self, event_key):
        if event_key == pygame.K_w:
            self.rect = self.rect.move(0, -self.dy)
        elif event_key == pygame.K_a:
            self.rect = self.rect.move(-self.dx, 0)
        elif event_key == pygame.K_s:
            self.rect = self.rect.move(0, self.dy)
        elif event_key == pygame.K_d:
            self.rect = self.rect.move(self.dx, 0)



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = w, h = 1920, 1080
ores = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Реакция на события от мыши')

board = Board(37, 20)
board.set_view(0, 0, 50)
hero = Hero(5, 5)
run = True
while run:
    screen.fill(BLACK)
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            hero.update_by_mouse(event.pos)
        if event.type == pygame.KEYDOWN:
            hero.update_by_keyboard(event.key)
    board.render(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()