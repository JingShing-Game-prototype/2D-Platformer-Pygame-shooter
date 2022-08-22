import pygame, numpy
from random import randint
from settings import resource_path, weapon_data, joystick
import os

class Weapon(pygame.sprite.Sprite):
    def __init__(self, groups, obstacle_sprite, user, target=None, type='ak74', create_blood_effect=None):
        super().__init__(groups)
        self.obstacle_sprite = obstacle_sprite
        self.create_blood_effect = create_blood_effect
        self.sprite_groups = groups
        self.object_type = 'weapon'
        self.type = type
        self.attack_type = 'ranged'
        self.user = user

        # attack mode
        self.can_melee_attack = True
        self.can_range_attack = True
            
        # melee part
        self.melee_attack = False
        self.melee_damage = 5
        self.or_melee_attack_direction = 1
        self.melee_attack_direction = self.or_melee_attack_direction
        # 1 means counter clockwise, -1 means clockwise
        self.or_melee_angle_speed = 5
        self.melee_angle_speed = self.or_melee_angle_speed
        # melee attack speed
        self.melee_angle = 0
        # count melee ratate angle
        self.melee_angle_range = 90
        # melee rotate range

        # gun info
        self.gun_shot_pos = None
        self.hold_legth = 0
        self.weapon_swing_rate = 10
        self.angle = 0

        self.target = target
        self.get_self_type_info()
        self.rect = self.or_image.get_rect(bottomright=self.user.rect.center)
        self.image = self.or_image.copy()


    def get_self_type_info(self):
        if os.path.exists('assets/graphics/weapon/' + self.type + '.png'):
            self.or_image = pygame.image.load(resource_path('assets/graphics/weapon/' + self.type + '.png')).convert_alpha()
        else:
            self.or_image = pygame.image.load(resource_path('assets/graphics/weapon/ak74.png')).convert_alpha()
        self.or_image = pygame.transform.scale(self.or_image, weapon_data[self.type]['size'])
        if 'melee_angle_speed' in weapon_data[self.type]:
            self.melee_angle_speed = weapon_data[self.type]['melee_angle_speed']
        else:
            self.melee_angle_speed = self.or_melee_angle_speed
        if 'melee_attack_cd' in weapon_data[self.type]:
            self.user.melee_attack_cd = weapon_data[self.type]['melee_attack_cd']
        else:
            self.user.melee_attack_cd = self.user.or_melee_attack_cd
        if 'melee_attack_direction' in weapon_data[self.type]:
            self.melee_attack_direction = weapon_data[self.type]['melee_attack_direction']
        else:
            self.melee_attack_direction = self.or_melee_attack_direction

    def adjust_pos(self):
        # get angle rotate and image pos
        if self.user.type == 'player':
            if self.user.joystick_aim:
                x = joystick.get_axis(2)
                y = joystick.get_axis(3)
            else:
                mouse_pos = pygame.mouse.get_pos()
                user_pos = self.user.offset_pos
                x = mouse_pos[0] - user_pos[0]
                y = mouse_pos[1] - user_pos[1]

        elif self.user.type == 'enemy':
            if self.target:
                target_pos = self.target.rect
                user_pos = self.user.rect
                x = target_pos[0] - user_pos[0]
                y = target_pos[1] - user_pos[1]
        
        self.user.flip = True if x < 0 else False
        angle = 0
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
        self.angle = angle
        self.image = pygame.transform.rotate(self.or_image, angle)

        # hold gun pos
        self.hold_gun_pos_get()
        
        # gun shot point
        x_bonus, y_bonus, gun_shot_x_rate, gun_shot_y_rate = self.get_gun_shot_point_pos_offset(x, y)

        if self.type == 'sword':
        # shoot from back
            self.gun_shot_pos = self.rect.center - 3 * pygame.math.Vector2(-self.image.get_width()/2 * gun_shot_x_rate + x_bonus, -self.image.get_height()/2 * gun_shot_y_rate + y_bonus + randint(-30, 30))
        else:
        # shoot from gun shot
            self.gun_shot_pos = self.rect.center + pygame.math.Vector2(-self.image.get_width()/2 * gun_shot_x_rate + x_bonus, -self.image.get_height()/2 * gun_shot_y_rate + y_bonus)

    def get_gun_shot_point_pos_offset(self, x, y):
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
        return x_bonus, y_bonus, gun_shot_x_rate, gun_shot_y_rate

    def hold_gun_pos_get(self):
        # hold gun pos
        x_offset, y_offset = self.multi_direction_spot_offset('gun')

        # hold gun pos
        if self.user.flip:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(midright=self.user.rect.midleft + pygame.math.Vector2(-self.hold_legth - x_offset, y_offset))
        else:
            self.rect = self.image.get_rect(midleft=self.user.rect.midright + pygame.math.Vector2(self.hold_legth + x_offset, y_offset))

    def multi_direction_spot_offset(self, mode='gun'):
        # multi angle fixed
        if mode == 'gun':
            if self.angle > 70:
                # up pos
                y_offset = -30
                x_offset = -30
            elif self.angle > 50:
                y_offset = -30
                x_offset = 10
            elif self.angle < -85:
                y_offset = 0
                x_offset = -30
            elif self.angle < -80:
                # down pos
                y_offset = 20
                x_offset = -30
            elif self.angle < -60:
                # down pos
                y_offset = 50
                x_offset = -10
            elif self.angle < -30:
                # down pos
                y_offset = 20
                x_offset = 5
            else:
                # mid pos
                y_offset = 0
                x_offset = 10
        elif mode == 'melee':
            if self.angle > 70:
                # up pos
                y_offset = -30
                x_offset = -30
            elif self.angle > 50:
                y_offset = -30
                x_offset = 10
            elif self.angle < -85:
                y_offset = 0
                x_offset = -30
            elif self.angle < -80:
                # down pos
                y_offset = 20
                x_offset = -30
            elif self.angle < -60:
                # down pos
                y_offset = 50
                x_offset = -10
            elif self.angle < -30:
                # down pos
                y_offset = 20
                x_offset = 5
            else:
                # mid pos
                y_offset = 0
                x_offset = 10

        return x_offset, y_offset

    def stick_on_user(self):
        self.rect = self.image.get_rect(center=self.user.rect.center)

    def touch_entity(self, entity):
        if entity.object_type != 'bullet':
            self.create_blood_effect(self.rect.center)
            if hasattr(entity, 'health'):
                entity.get_damage(self.melee_damage)
            if hasattr(entity, 'defense'):
                entity.defense = True
        else:
            if hasattr(entity, 'health'):
                entity.get_damage(self.melee_damage)
            else:
                entity.kill()

    def detect_entity(self):
        for sprite in self.obstacle_sprite:
            if sprite == self:
                pass
            elif sprite == self.user:
                pass
            elif sprite.object_type == 'entity':
                if sprite.rect.colliderect(self.rect):
                    self.touch_entity(sprite)
            elif sprite.object_type == 'bullet':
                if sprite.rect.colliderect(self.rect):
                    if sprite.direction.magnitude() != 0:
                        self.touch_entity(sprite)

    def melee_attack_animate(self):
        if self.user.type == 'enemy':
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
                self.angle = angle

        self.melee_angle += self.melee_angle_speed
        if self.melee_angle > self.melee_angle_range:
            self.melee_angle = 0
            self.melee_attack = False
        else:
            # self.image = pygame.transform.rotate(self.image, self.melee_angle * self.melee_attack_direction)
            self.image = pygame.transform.rotate(self.or_image, self.angle + self.melee_angle * self.melee_attack_direction)
            
            x_offset, y_offset = self.multi_direction_spot_offset('melee')

            if self.user.flip:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rect = self.image.get_rect(midright=self.user.rect.center + pygame.math.Vector2(-x_offset, y_offset))
            else:
                self.rect = self.image.get_rect(midleft=self.user.rect.center + pygame.math.Vector2(x_offset, y_offset))

    def shield(self):
        for sprite in self.obstacle_sprite:
            if sprite == self:
                pass
            elif sprite == self.user:
                pass
            elif sprite.object_type == 'bullet':
                if sprite.rect.colliderect(self.rect):
                    if sprite.direction.magnitude() != 0:
                        sprite.kill()

    def update(self):
        if self.type == 'shield':
            self.shield()
            self.adjust_pos()
        if self.melee_attack:
            self.melee_attack_animate()
            self.detect_entity()
        else:
            self.adjust_pos()