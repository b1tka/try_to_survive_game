import pygame
from different_funcs import csv_layout, import_cut_graphics
from objects import StaticTile, Crate, Border, Camera
from settings import tile_size, speed
from player import Player


class Level:
    def __init__(self, level_data, screen):
        self.screen = screen
        self.direction = pygame.math.Vector2(0, 0)
        self.level_l = pygame.sprite.Group()
        self.lock_y = False
        self.lock_x = False

        grass_l = csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_l, 'grass')

        water_l = csv_layout(level_data['water'])
        self.water_sprites = self.create_tile_group(water_l, 'water')

        cave_l = csv_layout(level_data['cave'])
        self.cave_sprites = self.create_tile_group(cave_l, 'cave')

        cave2_l = csv_layout(level_data['cave2'])
        self.cave2_sprites = self.create_tile_group(cave2_l, 'cave2')

        trees_l = csv_layout(level_data['trees'])
        self.trees_sprites = self.create_tile_group(trees_l, 'trees')

        door_l = csv_layout(level_data['door'])
        self.door_sprite = self.create_tile_group(door_l, 'door')

        bridge_l = csv_layout(level_data['bridge'])
        self.bridge_sprite = self.create_tile_group(bridge_l, 'bridge')

        self.horizontal_borders = pygame.sprite.Group()
        self.horizontal_borders.add(Border(0, 0, 3840, 1))
        self.horizontal_borders.add(Border(0, 2559, 3840, 1))

        self.vertical_borders = pygame.sprite.Group()
        self.vertical_borders.add(Border(0, 0, 1, 2560))
        self.vertical_borders.add(Border(3839, 0, 1, 2560))

        player = Player(self.vertical_borders, self.horizontal_borders)
        self.player = pygame.sprite.GroupSingle(player)

        self.camera = pygame.sprite.GroupSingle(Camera())

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'grass':
                        terrain_tile_list = import_cut_graphics(r'..\data\level_data\texture\grass.png')
                        grass_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, grass_surface)

                    elif type == 'water':
                        water_tile_list = import_cut_graphics(r'..\data\level_data\texture\water_texture.png')
                        water_surface = water_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, water_surface)

                    elif type == 'bridge':
                        bridge_tile_list = import_cut_graphics(r'..\data\level_data\texture\bridge.png')
                        bridge_surface = bridge_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, bridge_surface)

                    elif type == 'cave':
                        cave_tile_list = import_cut_graphics(r'..\data\level_data\texture\cave_pack.png',
                                                             size_x=160, size_y=160)
                        cave_surface = cave_tile_list[int(val)]
                        sprite = Crate(160, x, y, cave_surface)

                    elif type == 'cave2':
                        cave2_tile_list = import_cut_graphics(r'..\data\level_data\texture\cave_pack_2.png')
                        cave2_surface = cave2_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, cave2_surface)

                    elif type == 'trees':
                        trees_tile_list = import_cut_graphics(r'..\data\level_data\texture\tree.png',
                                                              size_x=128, size_y=170)
                        trees_surface = trees_tile_list[int(val)]
                        sprite = Crate(170, x, y, trees_surface, hitbox=True)

                    elif type == 'door':
                        door_tile_list = import_cut_graphics(r'..\data\level_data\texture\door.png',
                                                             size_x=92, size_y=113)
                        door_surface = door_tile_list[int(val)]
                        sprite = Crate(113, x, y, door_surface)

                    sprite_group.add(sprite)
                    self.level_l.add(sprite_group)
        return sprite_group

    def move(self):
        player = self.player.sprite
        keys = pygame.key.get_pressed()
        collide_x = pygame.sprite.spritecollide(self.camera.sprite, self.vertical_borders, False)
        if collide_x:
            if collide_x[0] == self.vertical_borders.sprites()[0] and player.rect.centerx <= 800:
                self.lock_x = True
                player.set_lock_x(False)
            elif collide_x[0] == self.vertical_borders.sprites()[-1] and player.rect.centerx >= 800:
                self.lock_x = True
                player.set_lock_x(False)
            else:
                self.lock_x = False
                player.set_lock_x(True)
                player.rect.centerx = 800
        else:
            self.lock_x = False
            player.set_lock_x(True)

        collide_y = pygame.sprite.spritecollide(self.camera.sprite, self.horizontal_borders, False)
        if collide_y:
            if collide_y[0] == self.horizontal_borders.sprites()[0] and player.rect.centery <= 450:
                self.lock_y = True
                player.set_lock_y(False)
            elif collide_y[0] == self.horizontal_borders.sprites()[-1] and player.rect.centery >= 450:
                self.lock_y = True
                player.set_lock_y(False)
            else:
                self.lock_y = False
                player.set_lock_y(True)
                player.rect.centery = 450
        else:
            self.lock_y = False
            player.set_lock_y(True)

        if not self.lock_y:
            if keys[pygame.K_w]:
                self.direction.y = 1
            elif keys[pygame.K_s]:
                self.direction.y = -1
            else:
                self.direction.y = 0
        else:
            self.direction.y = 0

        if not self.lock_x:
            if keys[pygame.K_a]:
                self.direction.x = 1
            elif keys[pygame.K_d]:
                self.direction.x = -1
            else:
                self.direction.x = 0
        else:
            self.direction.x = 0

    def texture_update(self, direction):
        self.grass_sprites.update(direction)
        self.water_sprites.update(direction)
        self.cave_sprites.update(direction)
        self.cave2_sprites.update(direction)
        self.trees_sprites.update(direction)
        self.door_sprite.update(direction)
        self.vertical_borders.update(direction)
        self.horizontal_borders.update(direction)
        self.bridge_sprite.update(direction)

    def check_collide(self):
        player = self.player.sprite
        trees = self.trees_sprites.sprites()
        if pygame.sprite.spritecollideany(self.player.sprite, self.water_sprites) or \
                pygame.sprite.spritecollideany(self.player.sprite, self.cave_sprites) or \
                pygame.sprite.spritecollideany(self.player.sprite, self.cave2_sprites):
            self.texture_update(self.direction * speed * -1)
            self.player.update(back=True)
        for tree in trees:
            if tree.hitbox[0] - 10 < player.rect.centerx < tree.hitbox[0] + tree.hitbox[2] + 10 and \
                    tree.hitbox[1] - 10 < player.rect.centery < tree.hitbox[1] + tree.hitbox[3] + 10:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_e]:
                    player.destroy_object(tree)
            if tree.hitbox[0] < player.rect.centerx < tree.hitbox[0] + tree.hitbox[2] and \
                    tree.hitbox[1] < player.rect.centery < tree.hitbox[1] + tree.hitbox[3]:
                self.texture_update(self.direction * speed * -1)
                self.player.update(back=True)

    def run(self):
        self.move()
        self.player.sprite.move()
        self.texture_update(self.direction * speed)
        self.player.update()
        self.check_collide()

        self.level_l.draw(self.screen)
        self.player.draw(self.screen)
        self.camera.draw(self.screen)
