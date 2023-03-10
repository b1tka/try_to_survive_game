import pygame
from game_data import hero, items
from settings import speed
from different_funcs import csv_layout, import_cut_graphics, rotate_frames
from objects import StaticTile, Crate, TreeInventory, StoneInventory, CellCraft, SwordInventory
from settings import tile_size
from game_data import inventory


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, camera):
        super().__init__()
        self.frames_behind = import_cut_graphics(hero['w'], size_x=60, size_y=93)
        self.frames_left = import_cut_graphics(hero['a'], size_x=60, size_y=93)
        self.frames_right = import_cut_graphics(hero['d'], size_x=60, size_y=93)
        self.frames_forward = import_cut_graphics(hero['s'], size_x=60, size_y=93)
        self.cur_frame = 0
        self.camera = camera
        self.rect = self.frames_forward[1].get_rect()
        self.vision = 'forward'
        self.direction = pygame.math.Vector2(0, 0)
        self.rect.centerx = 800
        self.rect.centery = 450
        self.x_lock = True
        self.y_lock = True
        self.healthpoints = 10
        self.inventory = Inventory(screen)
        self.attack_group = pygame.sprite.Group()

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

    def get_damage(self):
        self.healthpoints -= 1
        self.camera.update_hp(self.healthpoints)
        if self.healthpoints == 0:
            self.end_game()

    def end_game(self):
        if self.healthpoints == 0:
            return True
        return False

    def attack(self):
        if self.inventory.is_sword():
            self.attack_group.add(Attack(self.rect.x, self.rect.y, self.vision))

    def reset_direction(self):
        self.direction.x = 0
        self.direction.y = 0

    def update(self, back=False):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.cur_frame += 1
            self.vision = 'behind'
            self.image = self.frames_behind[self.cur_frame // 15 % 3]
        elif keys[pygame.K_a]:
            self.cur_frame += 1
            self.vision = 'left'
            self.image = self.frames_left[self.cur_frame // 15 % 3]
        elif keys[pygame.K_s]:
            self.cur_frame += 1
            self.vision = 'forward'
            self.image = self.frames_forward[self.cur_frame // 15 % 3]
        elif keys[pygame.K_d]:
            self.cur_frame += 1
            self.vision = 'right'
            self.image = self.frames_right[self.cur_frame // 15 % 3]
        else:
            if self.vision == 'behind':
                self.image = self.frames_behind[0]
            if self.vision == 'left':
                self.image = self.frames_left[0]
            if self.vision == 'right':
                self.image = self.frames_right[0]
            if self.vision == 'forward':
                self.image = self.frames_forward[0]
        self.cur_frame = self.cur_frame % 45
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
        self.all_resources = {
            'tree': 0,
            'stone': 0,
            'sword': 0
        }
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

    def check_craft(self):
        possible_items = list()
        for item in items.keys():
            keys = items[item].keys()
            need = len(keys)
            have = 0
            for object in keys:
                if self.all_resources[object] >= items[item][object]:
                    have += 1
            if have == need:
                possible_items.append(item)

        if len(possible_items) == 0:
            return None
        return possible_items

    def craft(self, object, amount):
        self.add_item(object, amount)
        resource = items[object]
        for key in resource:
            self.all_resources[key] -= resource[key]
        for key in resource:
            object = key
            if resource[object] <= 0:
                for i in range(len(self.inventory)):
                    for j in range(len(self.inventory[i])):
                        if self.inventory[i][j][0] == object:
                            ostatok = resource[object] - self.inventory[i][j][1]
                            if ostatok < 0:
                                self.inventory[i][j][1] = self.inventory[i][j][1] - resource[object]
                                resource[object] = ostatok
                            else:
                                self.inventory[i][j] = ['NonObject', 0]
                                resource[object] = 0

    def add_item(self, object, amount):
        is_break = False
        self.all_resources[object] += amount
        for i in range(len(self.inventory)):
            for j in range(len(self.inventory[i])):
                if self.inventory[i][j][0] != object and self.inventory[i][j][0] != 'NonObject':
                    continue
                elif self.inventory[i][j][0] == object and self.inventory[i][j][1] <= 3:
                    if self.inventory[i][j][1] == 3:
                        continue
                    elif self.inventory[i][j][1] + amount > 3:
                        amount = (self.inventory[i][j][1] + amount) % 3
                        self.inventory[i][j][1] = 3
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

    def is_sword(self):
        if self.all_resources['sword']:
            return True
        return False

    def run(self):
        self.cell_sprite.draw(self.screen)
        self.hero_sprite.draw(self.screen)
        craft = self.check_craft()
        if craft:
            for i in range(len(craft)):
                pygame.sprite.GroupSingle(CellCraft(0, i * 2, craft[i])).draw(self.screen)
            if pygame.key.get_pressed()[pygame.K_c]:
                self.craft('sword', 1)
        for i in range(len(self.inventory)):
            for j in range(len(self.inventory[i])):
                if self.inventory[j][i][0] == 'tree':
                    pygame.sprite.GroupSingle(TreeInventory(i, j, self.inventory[j][i][-1])).draw(self.screen)
                elif self.inventory[j][i][0] == 'stone':
                    pygame.sprite.GroupSingle(StoneInventory(i, j, self.inventory[j][i][-1])).draw(self.screen)
                elif self.inventory[j][i][0] == 'sword':
                    pygame.sprite.GroupSingle(SwordInventory(i, j, self.inventory[j][i][-1])).draw(self.screen)


class Attack(pygame.sprite.Sprite):
    def __init__(self, x, y, vision):
        super().__init__()
        self.attack_frames = import_cut_graphics(r'..\data\player_data\attack_silver.png', size_x=136, size_y=158)
        self.cur_frame = 0
        if vision == 'right':
            self.x = x + 60
            self.y = y
        elif vision == 'left':
            self.x = x - 120
            self.y = y
        elif vision == 'forward':
            self.y = y + 90
            self.x = x - 46
        elif vision == 'behind':
            self.x = x - 46
            self.y = y - 90
        self.vision = vision

    def update(self):
        self.cur_frame += 1
        if self.vision == 'right':
            self.frames = self.attack_frames
        elif self.vision == 'behind':
            self.frames = rotate_frames(self.attack_frames, 90)
        elif self.vision == 'left':
            self.frames = rotate_frames(self.attack_frames, 180)
        elif self.vision == 'forward':
            self.frames = rotate_frames(self.attack_frames, 270)
        self.image = self.frames[self.cur_frame // 2]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if self.cur_frame == 8:
            self.kill()