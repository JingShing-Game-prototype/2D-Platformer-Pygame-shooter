import pygame, numpy
from random import randint
class Weapon(pygame.sprite.Sprite):
    def __init__(self, groups, user):
        super().__init__(groups)
        self.object_type = 'weapon'
        self.or_image = pygame.image.load('assets\graphics\weapon\Ak74.png').convert_alpha()
        self.or_image = pygame.transform.scale(self.or_image, (96, 32))
        # self.or_image = pygame.Surface((48, 16))
        self.color = (255, 0, 0)
        # self.or_image.fill(self.color)
        self.user = user
        self.rect = self.or_image.get_rect(center=self.user.rect.center)
        self.image = self.or_image.copy()
        self.flip = False

    def adjust_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        user_pos = self.user.offset_pos
        x = mouse_pos[0] - user_pos[0]
        y = mouse_pos[1] - user_pos[1]
        self.flip = True if x < 0 else False
        if x!=0 and y!=0:
            angle = (numpy.arctan(y/x) * 180 / 3.14)
            if self.user.using_weapon:
                angle += randint(-20, 20)
            if not self.flip:
                angle = -angle
        else:
            angle = 0
        self.image = pygame.transform.rotate(self.or_image, angle)
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=self.user.rect.center)

    def stick_on_user(self):
        self.rect = self.image.get_rect(center=self.user.rect.center)

    def update(self):
        self.adjust_pos()
        self.stick_on_user()