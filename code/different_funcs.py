import csv
import pygame
from math import sqrt, sin, asin, degrees
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


def find_coefficient_and_angle(x1, y1, x2, y2):
    x1_rev, y1_rev = x1 * -1, y1 * -1
    x3 = x1_rev + x2
    y3 = y1_rev + y2
    try:
        k = y3 / x3
    except ZeroDivisionError:
        k = 0
    b = y1 - k * x1

    len_hypotinues = sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)
    if x1 > x2 and y1 > x2:
        angle = degrees(asin(sin(abs(x1 - x2) / len_hypotinues)))
    elif x1 < x2 and y1 > y2:
        angle = degrees(asin(sin(abs(y1 - y2) / len_hypotinues))) + 270
    elif x1 > x2 and y1 < y2:
        angle = degrees(asin(sin(abs(y1 - y2) / len_hypotinues))) + 90
    elif x1 < x2 and y1 < y2:
        angle = degrees(asin(sin(abs(x1 - x2) / len_hypotinues))) + 180
    elif x1 == x2:
        if y1 < y2:
            angle = 180
        else:
            angle = 0
    elif y1 == y2:
        if x1 < x2:
            angle = 270
        else:
            angle = 90
    else:
        angle = 0

    return k, b, angle


def rotate_frames(frames, angle):
    new_frames = list()
    for frame in frames:
        new_frame = pygame.transform.rotate(frame, angle)
        new_frames.append(new_frame)
    return new_frames
