import pygame
from different_funcs import import_cut_graphics, find_coefficient_and_angle, rotate_frames
from settings import w, h, tile_size
from game_data import items_path
from random import randint


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

    def update(self, vector):
        self.rect.center += vector


class StaticTile(Tile):
    def __init__(self, size, pos_x, pos_y, surface):
        super().__init__(size, pos_x, pos_y)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, size, pos_x, pos_y, surface, object=None, hitbox=False):
        super().__init__(size, pos_x, pos_y, surface)
        offset_y = pos_y + 64
        self.rect = self.image.get_rect(bottomleft=(pos_x, offset_y))
        self.is_hitbox = hitbox
        if hitbox:
            self.hitbox = [pos_x + 32, pos_y + 32, 64, 32]
            self.resource = (randint(1, 3), object)

    def get_resource(self):
        return self.resource

    def update(self, vector):
        super().update(vector)
        if self.is_hitbox:
            self.hitbox[0] += vector.x
            self.hitbox[1] += vector.y


class Book(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = import_cut_graphics(r'..\data\level_data\texture\book.png', size_x=88, size_y=79)[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = -100
        self.rect.centery = -100

    def activate(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def update(self, vector):
        self.rect.center += vector


class Border(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill('white')
        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = top

    def get_rect(self):
        return self.rect

    def update(self, vector):
        self.rect.center += vector


class Camera(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((w, h), flags=pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.hp_bar = pygame.Surface((400, 40))
        pygame.draw.rect(self.hp_bar, 'red', (0, 0, 400, 40))
        pygame.draw.rect(self.hp_bar, 'white', (0, 0, 400, 40), 1)
        self.image.blit(self.hp_bar, (10, 10))
        font = pygame.font.Font(r'../data/fonts/retro-land-mayhem.ttf', 20)
        text = font.render('Press E for destroy', True, (225, 225, 0))
        self.image.blit(text, (675, 750))

    def update_hp(self, healthpoints):
        percent = healthpoints / 10
        pygame.draw.rect(self.hp_bar, 'black', (0, 0, 400, 40))
        pygame.draw.rect(self.hp_bar, 'red', (0, 0, 400 * percent, 40))
        pygame.draw.rect(self.hp_bar, 'white', (0, 0, 400, 40), 1)
        self.image.blit(self.hp_bar, (10, 10))



class ObjInv(pygame.sprite.Sprite):
    def __init__(self, x, y, path, amount=None):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.center += pygame.Vector2(700, 428)
        self.rect.x += tile_size * x
        self.rect.y += tile_size * y
        if amount:
            font = pygame.font.Font(r'../data/fonts/retro-land-mayhem.ttf', 20)
            text = font.render(str(amount), True, 'green')
            self.image.blit(text, (40, 40))


class TreeInventory(ObjInv):
    def __init__(self, x, y, amount):
        super().__init__(x, y, r'..\data\level_data\texture\log.png', amount)


class StoneInventory(ObjInv):
    def __init__(self, x, y, amount):
        super().__init__(x, y, r'..\data\level_data\texture\stone_inv.png', amount)


class SwordInventory(ObjInv):
    def __init__(self, x, y, amount):
        super().__init__(x, y, r'D:\PyGameProject\data\level_data\texture\sword.png', amount)


class CellCraft(ObjInv):
    def __init__(self, x, y, type):
        super().__init__(x, y, r'..\data\level_data\texture\craft_cell.png')
        self.rect.x += tile_size * 4 + 1
        self.rect.y -= tile_size * 2
        self.image.blit(pygame.image.load(items_path[type]), (0, 0))


class FireBall(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.speed = 3
        self.cur_frame = 0
        if x1 < x2:
            self.rotation = 'left'
        elif x1 > x2:
            self.rotation = 'right'
        elif x1 == x2:
            if y1 > y2:
                self.rotation = 'up'
            else:
                self.rotation = 'down'
        k, b, angle = find_coefficient_and_angle(x1, y1, x2, y2)
        self.k = k
        self.b = b
        self.frames = rotate_frames(import_cut_graphics(r'D:\PyGameProject\data\dragon_data\fireball.png',
                                                        size_x=128, size_y=128), angle)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x2
        self.rect.centery = y2

    def update(self, vector):
        if self.rotation == 'left':
            self.rect.centerx += self.speed * -1
            self.rect.centery = self.rect.centerx * self.k + self.b
        elif self.rotation == 'right':
            self.rect.centerx += self.speed
            self.rect.centery = self.rect.centerx * self.k + self.b
        elif self.rotation == 'up':
            self.rect.centerx += 0
            self.rect.centery += self.speed
        elif self.rotation == 'down':
            self.rect.centerx += 0
            self.rect.centery -= self.speed
        print(self.rect.centerx, self.rect.centery)

        if self.rect.centery < 0 or self.rect.centerx < 0 or self.rect.centerx > 1500 \
            or self.rect.centery > 2000:
            self.kill()
        self.cur_frame += 1
        self.cur_frame = self.cur_frame % 18
        self.image = self.frames[self.cur_frame // 3]

        self.rect.center += vector