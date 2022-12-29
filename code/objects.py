import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

    def update(self, shift):
        self.rect.x += shift
        self.rect.y -= 3


class StaticTile(Tile):
    def __init__(self, size, pos_x, pos_y, surface):
        super().__init__(size, pos_x, pos_y)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, size, pos_x, pos_y, surface):
        super().__init__(size, pos_x, pos_y, surface)
        offset_y = pos_y + 64
        self.rect = self.image.get_rect(bottomleft=(pos_x, offset_y))
