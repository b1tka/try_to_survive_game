import pygame
from game_data import hero
from settings import speed


class Player(pygame.sprite.Sprite):
    def __init__(self, vertical_borders, horizontal_borders):
        super().__init__()
        self.image = pygame.Surface((64, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.direction = pygame.math.Vector2(0, 0)
        self.rect.centerx = 800
        self.rect.centery = 450
        self.x_lock = True
        self.y_lock = True
        self.vertical_borders = vertical_borders
        self.horizontal_borders = horizontal_borders
        self.healthpoints = 5

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

        if pygame.sprite.spritecollideany(self, self.vertical_borders):
            self.rect.centerx += self.direction.x * speed * -1
        if pygame.sprite.spritecollideany(self, self.horizontal_borders):
            self.rect.centery += self.direction.y * speed * -1
