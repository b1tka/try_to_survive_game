import pygame
from different_funcs import find_coefficient_and_angle, rotate_frames, import_cut_graphics
from objects import FireBall
from game_data import dragon


class Dragon(pygame.sprite.Sprite):
    def __init__(self, screen, player, book):
        super().__init__()
        self.frames = import_cut_graphics(dragon, size_x=256, size_y=256)
        self.image = self.frames[0]
        self.speed = 4
        self.hitbox = list()
        self.player = player
        self.book = book
        self.hp = 40
        self.fireballs_group = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.screen = screen
        self.cur_frame = 0
        self.cd = 0

    def change_picture(self, collide=False):
        if collide:
            x1, y1 = self.player.rect.centerx, self.player.rect.centery
            x2, y2 = self.rect.centerx, self.rect.centery
            k, b, angle = find_coefficient_and_angle(x1, y1, x2, y2)
            if x1 > x2:
                self.rect.centerx += self.speed
                self.rect.centery = self.rect.centerx * k + b
            elif x1 < x2:
                self.rect.centerx += self.speed * -1
                self.rect.centery = self.rect.centerx * k + b
            elif x1 == x2:
                self.rect.centerx += self.speed * 0
                if y1 < y2:
                    self.rect.centery -= self.speed
                else:
                    self.rect.centery += self.speed
            self.cur_frame += 1
            self.cur_frame = self.cur_frame % 20
            frames = rotate_frames(self.frames, angle)
            self.image = frames[self.cur_frame // 10 + 1]
            self.cd += 1
            self.cd = self.cd % 181
            if self.cd == 180:
                self.attack_fireball()
        else:
            self.image = self.frames[0]

    def attack_fireball(self):
        x1, y1 = self.player.rect.centerx, self.player.rect.centery
        x2, y2 = self.rect.centerx, self.rect.centery
        self.fireballs_group.add(FireBall(x1, y1, x2, y2))

    def get_damage(self):
        self.image = pygame.image.load(r'..\data\dragon_data\dragon_damage.png')
        self.hp = self.hp - 1
        if self.hp == 0:
            for fireball in self.fireballs_group.sprites():
                fireball.kill()
            self.drop_book()
            self.kill()

    def drop_book(self):
        self.book.activate(self.rect.centerx, self.rect.centery)

    def update(self, vector, collide=False):
        self.rect.center += vector
        self.fireballs_group.update(vector)
        self.hitbox = [self.rect.centerx, self.rect.centery]