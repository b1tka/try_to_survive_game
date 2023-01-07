import csv
import pygame
from settings import tile_size


def csv_layout(path):
    map = list()
    with open(path) as csvfile:
        level = csv.reader(csvfile, delimiter=',')
        for row in level:
            map.append(row)
    return map


def import_cut_graphics(path, size_x=tile_size, size_y=tile_size):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / size_x)
    tile_num_y = int(surface.get_size()[1] / size_y)
    cut_tiles = list()

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * size_x
            y = row * size_y
            new_surf = pygame.Surface((size_x, size_y), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, size_x, size_y))
            cut_tiles.append(new_surf)

    return cut_tiles