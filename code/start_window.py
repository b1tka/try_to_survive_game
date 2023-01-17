import pygame
from different_funcs import import_cut_graphics


class WinSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(r'..\data\window\start_window.png')
        self.play = import_cut_graphics(r'..\data\window\play.png', size_x=392, size_y=66)[0]
        self.image.blit(self.play, (620, 700))
        self.rect = self.image.get_rect()

    def check_collide(self, pos):
        if 620 < pos[0] < 1012 and 700 < pos[1] < 766:
            return True
        return False


class StartWindow:
    def __init__(self, screen):
        self.window = pygame.sprite.GroupSingle(WinSprite())
        self.screen = screen

    def check_pressed(self, pos):
        if self.window.sprite.check_collide(pos):
            return True
        return False

    def run(self):
        self.window.draw(self.screen)


class End:
    def __init__(self, screen):
        self.window = pygame.sprite.GroupSingle(WinSprite())
        self.window.sprite.image = pygame.image.load('..\data\window\game_over.png')
        self.window.sprite.rect.centerx = 800
        self.window.sprite.rect.centery = 450
        self.screen = screen

    def run(self):
        self.window.draw(self.screen)
