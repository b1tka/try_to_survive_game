import pygame
from settings import w, h


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
    def __init__(self, size, pos_x, pos_y, surface, hitbox=False):
        super().__init__(size, pos_x, pos_y, surface)
        offset_y = pos_y + 64
        self.rect = self.image.get_rect(bottomleft=(pos_x, offset_y))
        self.hitbox = hitbox
        if self.hitbox:
            self.hitbox = [pos_x + 16, pos_y, 96]

    def update(self, vector):
        super().update(vector)
        if self.hitbox:
            self.hitbox[0] += vector.x
            self.hitbox[1] += vector.y

class Border(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height):
        super().__init__()
        self.rect = pygame.Rect(left, top, width, height)

    def get_rect(self):
        return self.rect

    def update(self, vector):
        self.rect.center += vector


class Camera(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((w, h), flags=pygame.SRCALPHA)
        self.image.set_colorkey((244, 208, 63))
        self.rect = self.image.get_rect()
        self.hp_bar = pygame.Surface((400, 40))
        pygame.draw.rect(self.hp_bar, 'red', (0, 0, 400, 40))
        pygame.draw.rect(self.hp_bar, 'white', (0, 0, 400, 40), 1)
        self.image.blit(self.hp_bar, (10, 10))
        font = pygame.font.Font(r'..\data\fonts\retro-land-mayhem.ttf', 20)
        text = font.render('Press E', True, (244, 208, 63))
        self.image.blit(text, (750, 675))

    def want_to_do_action(self, state):
        pass
        if state:
            self.image.set_colorkey((244, 208, 64))
        else:
            self.image.set_colorkey((244, 208, 63))