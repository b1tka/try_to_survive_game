import pygame
from game_data import hero
from settings import speed
from different_funcs import csv_layout, import_cut_graphics
from objects import StaticTile, Crate, TreeInventory, StoneInventory
from settings import tile_size
from game_data import inventory


class Player(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.Surface((64, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.direction = pygame.math.Vector2(0, 0)
        self.rect.centerx = 800
        self.rect.centery = 450
        self.x_lock = True
        self.y_lock = True
        self.healthpoints = 5
        self.inventory = Inventory(screen)

    def move(self):
        keys = pygame.key.get_pressed()

        if not self.y_lock:
            if keys[pygame.K_w]:
                self.direction.y = -1
            elif keys[pygame.K_s]:
                self.direction.y = 1
            else:
                self.direction.y = 0
        else:
            self.direction.y = 0

        if not self.x_lock:
            if keys[pygame.K_a]:
                self.direction.x = -1
            elif keys[pygame.K_d]:
                self.direction.x = 1
            else:
                self.direction.x = 0
        else:
            self.direction.x = 0

    def destroy_object(self, object):
        resource = object.get_resource()
        self.inventory.add_item(resource[1], resource[0])
        object.kill()

    def set_lock_x(self, status):
        self.x_lock = status

    def set_lock_y(self, status):
        self.y_lock = status

    def get_rect(self):
        return self.rect

    def reset_direction(self):
        self.direction.x = 0
        self.direction.y = 0

    def update(self, back=False):
        if back:
            self.rect.center += self.direction * speed * -1
        else:
            self.rect.center += self.direction * speed


class Inventory(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        cell_item = csv_layout(inventory['cells'])
        self.cell_sprite = self.create_tile_group(cell_item, 'cell')
        self.cell_sprite.update(pygame.math.Vector2(700, 300))
        self.inventory = list()
        for _ in range(4):
            time_list = list()
            for _ in range(4):
                time_list.append(['NonObject', 0])
            self.inventory.append(time_list)

        hero = csv_layout(inventory['hero'])
        self.hero_sprite = self.create_tile_group(hero, 'hero')
        self.hero_sprite.update(pygame.math.Vector2(700, 300))

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'cell':
                        cells_tile_list = import_cut_graphics(r'..\data\level_data\texture\invetory_cells.png')
                        cells_surface = cells_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, cells_surface)

                    elif type == 'hero':
                        hero_tile_list = import_cut_graphics(r'..\data\level_data\texture\inventory_hero.png',
                                                             size_x=128, size_y=128)
                        hero_surface = hero_tile_list[int(val)]
                        sprite = Crate(128, x, y, hero_surface)

                    sprite_group.add(sprite)

        return sprite_group

    def add_item(self, object, amount):
        is_break = False
        print(amount)
        for i in range(len(self.inventory)):
            for j in range(len(self.inventory[i])):
                if self.inventory[i][j][0] != object and self.inventory[i][j][0] != 'NonObject':
                    continue
                elif self.inventory[i][j][0] == object and self.inventory[i][j][1] <= 6:
                    if self.inventory[i][j][1] == 6:
                        continue
                    elif self.inventory[i][j][1] + amount > 6:
                        amount = (self.inventory[i][j][1] + amount) % 6
                        self.inventory[i][j][1] = 6
                    else:
                        self.inventory[i][j][1] += amount
                        is_break = True
                        break
                else:
                    self.inventory[i][j][0] = object
                    self.inventory[i][j][1] = amount
                    is_break = True
                    break
            if is_break:
                break

    def run(self):
        self.cell_sprite.draw(self.screen)
        self.hero_sprite.draw(self.screen)
        for i in range(len(self.inventory)):
            for j in range(len(self.inventory[i])):
                if self.inventory[j][i][0] == 'tree':
                    pygame.sprite.GroupSingle(TreeInventory(i, j, self.inventory[j][i][-1])).draw(self.screen)
                elif self.inventory[j][i][0] == 'stone':
                    pygame.sprite.GroupSingle(StoneInventory(i, j, self.inventory[j][i][-1])).draw(self.screen)
