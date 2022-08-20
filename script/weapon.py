import pygame, numpy
from random import randint
class Weapon(pygame.sprite.Sprite):
    def __init__(self, groups, user, target=None, type='ak74'):
        super().__init__(groups)
        self.object_type = 'weapon'
        self.type = type
        if self.type == 'ak74':
            self.or_image = pygame.image.load('assets\graphics\weapon\Ak74_rot.png').convert_alpha()
            self.or_image = pygame.transform.scale(self.or_image, (96, 32))
        if self.type == 'bullet':
            self.or_image = pygame.image.load('assets\graphics\weapon\\bullet_s.png').convert_alpha()
            self.or_image = pygame.transform.scale(self.or_image, (32, 16))
            
        # self.or_image = pygame.Surface((48, 16))
        self.color = (255, 0, 0)
        # self.or_image.fill(self.color)
        self.user = user
        self.target = target
        self.rect = self.or_image.get_rect(bottomright=self.user.rect.center)
        self.image = self.or_image.copy()
        self.gun_shot_pos = None
        self.hold_legth = 0
        self.weapon_swing_rate = 10

    def adjust_pos(self):
        if self.user.object_type == 'player':
            mouse_pos = pygame.mouse.get_pos()
            user_pos = self.user.offset_pos
            x = mouse_pos[0] - user_pos[0]
            y = mouse_pos[1] - user_pos[1]
            self.user.flip = True if x < 0 else False
            if x!=0 and y!=0:
                angle = numpy.arctan(y/x) * 180 / 3.14
                if self.user.using_weapon:
                    angle += randint(-self.weapon_swing_rate, self.weapon_swing_rate)
                if not self.user.flip:
                    angle = -angle
            elif x==0:
                if y < 0:
                    angle = 90
                elif y > 0:
                    angle = 270
            else:
                angle = 0
            self.image = pygame.transform.rotate(self.or_image, angle)
            # hold gun pos
            if self.user.flip:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.image.get_rect(midright=self.user.rect.midleft + pygame.math.Vector2(-self.hold_legth, 0))
            else:
                self.rect = self.image.get_rect(midleft=self.user.rect.midright + pygame.math.Vector2(self.hold_legth, 0))
            
            # gun shot point pos
            if self.user.flip:
                gun_shot_x_rate = 1
                x_bonus = 0
            else:
                gun_shot_x_rate = -1
                x_bonus = 0
            if x == 0:
                gun_shot_x_rate = 0
                x_bonus = 0
            if y > 0:
                gun_shot_y_rate = -1
                y_bonus = -10
            elif y < 0:
                gun_shot_y_rate = 1
                y_bonus = 10
            elif y == 0:
                gun_shot_y_rate = 0
                y_bonus = 0
            self.gun_shot_pos = self.rect.center + pygame.math.Vector2(-self.image.get_width()/2 * gun_shot_x_rate + x_bonus, -self.image.get_height()/2 * gun_shot_y_rate + y_bonus)

        elif self.user.object_type == 'enemy':
            if self.target:
                target_pos = self.target.rect
                user_pos = self.user.rect
                x = target_pos[0] - user_pos[0]
                y = target_pos[1] - user_pos[1]
                self.user.flip = True if x < 0 else False
                if x!=0 and y!=0:
                    angle = (numpy.arctan(y/x) * 180 / 3.14)
                    if self.user.using_weapon:
                        angle += randint(-self.weapon_swing_rate, self.weapon_swing_rate)
                    if not self.user.flip:
                        angle = -angle
                elif x==0:
                    angle = 90
                else:
                    angle = 0
                self.image = pygame.transform.rotate(self.or_image, angle)
                if self.user.flip:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.rect = self.image.get_rect(midright=self.user.rect.midleft + pygame.math.Vector2(-self.hold_legth, 0))
                else:
                    self.rect = self.image.get_rect(midleft=self.user.rect.midright + pygame.math.Vector2(self.hold_legth, 0))
                
                if self.user.flip:
                    gun_shot_x_rate = 1
                    x_bonus = 0
                else:
                    gun_shot_x_rate = -1
                    x_bonus = 0
                if x == 0:
                    gun_shot_x_rate = 0
                    x_bonus = 0

                if y > 0:
                    gun_shot_y_rate = -1
                    y_bonus = -10
                elif y < 0:
                    gun_shot_y_rate = 1
                    y_bonus = 10
                elif y == 0:
                    gun_shot_y_rate = 0
                    y_bonus = 0
                self.gun_shot_pos = self.rect.center + pygame.math.Vector2(-self.image.get_width()/2 * gun_shot_x_rate + x_bonus, -self.image.get_height()/2 * gun_shot_y_rate + y_bonus)


    def stick_on_user(self):
        self.rect = self.image.get_rect(center=self.user.rect.center)

    def update(self):
        self.adjust_pos()
        # self.stick_on_user()