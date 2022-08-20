import pygame
from settings import screen_height, screen_width
import numpy

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, type='ak_bullet', direction=pygame.math.Vector2(0, 0), speed = 0.1, create_blood_effect=None):
        super().__init__(groups)
        self.object_type = 'bullet'
        self.type = type
        self.obstacle_sprites = obstacle_sprites
        self.direction = direction
        self.create_blood_effect = create_blood_effect
        self.flip = True if self.direction.x < 0 else False
        self.angle = self.adjust_angle()
        if self.type == 'ak_bullet':
            self.image = pygame.image.load('assets\graphics\weapon\\bullet_s.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (16, 8))
        self.image = pygame.transform.rotate(self.image, self.angle)
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.damage = 1

    def adjust_angle(self):
        x = self.direction.x
        y = self.direction.y
        if x!=0 and y!=0:
            angle = (numpy.arctan(y/x) * 180 / 3.14)
            if not self.flip:
                angle = -angle
        elif x == 0:
            angle = 90
        else:
            angle = 0

        return angle

    def touch_target(self, target):
        if self.direction.magnitude() != 0:
            if target.object_type != 'bullet':
                self.create_blood_effect(self.rect.center)
                if hasattr(target, 'health'):
                    target.get_damage(self.damage)
                if hasattr(target, 'defense'):
                    target.defense = True
            self.kill() # kill bullet when bullet bump

    def no_move(self):
        self.direction.x = 0
        self.direction.y = 0

    def object_movement_collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite == self:
                pass
            elif sprite.object_type == 'player':
                if sprite.rect.colliderect(self.rect):
                    self.touch_target(sprite)
            elif sprite.object_type == 'enemy':
                if sprite.rect.colliderect(self.rect):
                    self.touch_target(sprite)
            elif sprite.object_type == 'bullet':
                if sprite.rect.colliderect(self.rect):
                    if sprite.direction.magnitude() != 0:
                        self.touch_target(sprite)
            else:
                if direction == 'horizontal':
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.x < 0:
                            self.rect.left = sprite.rect.right
                            self.no_move()
                        if self.direction.x > 0:
                            self.rect.right = sprite.rect.left
                            self.no_move()
                elif direction == 'vertical':
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.y > 0:
                            self.rect.bottom = sprite.rect.top
                            self.no_move()
                        elif self.direction.y < 0:
                            self.rect.top = sprite.rect.bottom
                            self.no_move()

    def move(self):
        if self.direction.magnitude() != 0:
            # 0 can't be normalized. python will error.
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * self.speed
        self.object_movement_collision(direction='horizontal')
        self.rect.y += self.direction.y * self.speed
        self.object_movement_collision(direction='vertical')

    def update(self):
        self.move()