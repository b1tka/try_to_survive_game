import pygame
from different_funcs import csv_layout, import_cut_graphics
from objects import StaticTile, Crate
from settings import tile_size


class Level:
    def __init__(self, level_data, surface):
        self.surface = surface
        self.global_shift = -10

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
                        sprite = Crate(170, x, y, trees_surface)

                    elif type == 'door':
                        door_tile_list = import_cut_graphics(r'..\data\level_data\texture\door.png',
                                                             size_x=92, size_y=113)
                        door_surface = door_tile_list[int(val)]
                        sprite = Crate(113, x, y, door_surface)

                    sprite_group.add(sprite)
        return sprite_group

    def run(self, screen):
        self.grass_sprites.update(self.global_shift)
        self.grass_sprites.draw(screen)

        self.water_sprites.update(self.global_shift)
        self.water_sprites.draw(screen)

        self.cave2_sprites.update(self.global_shift)
        self.cave2_sprites.draw(screen)

        self.cave_sprites.update(self.global_shift)
        self.cave_sprites.draw(screen)

        self.trees_sprites.update(self.global_shift)
        self.trees_sprites.draw(screen)

        self.door_sprite.update(self.global_shift)
        self.door_sprite.draw(screen)