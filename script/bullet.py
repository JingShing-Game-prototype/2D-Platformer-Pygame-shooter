import pygame
from settings import map_height, map_width, resource_path
import numpy
import os

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, type='ak74', direction=pygame.math.Vector2(0, 0), speed = 0.1, create_blood_effect=None, user=None, across_wall=False):
        super().__init__(groups)
        self.object_type = 'bullet'
        self.across_wall = across_wall
        self.type = type
        self.user = user
        self.obstacle_sprites = obstacle_sprites
        self.direction = direction
        self.create_blood_effect = create_blood_effect
        self.flip = True if self.direction.x < 0 else False
        self.angle = self.adjust_angle()
        self.get_self_type_info()
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

        # bullet damage and health
        self.health = 10
        self.damage = 30

    def get_self_type_info(self):
        if os.path.exists('assets/graphics/weapon/' + self.type + '.png'):
            self.image = pygame.image.load(resource_path('assets/graphics/weapon/' + self.type + '.png')).convert_alpha()
        else:
            self.image = pygame.image.load(resource_path('assets/graphics/weapon/ak74.png')).convert_alpha()
        if self.type == 'bullet':
            self.image = pygame.transform.scale(self.image, (16, 8))
        if self.type == 'ak74':
            self.image = pygame.transform.scale(self.image, (80, 24))
        if self.type == 'sword':
            self.image = pygame.transform.scale(self.image, (100, 30))
        self.image = pygame.transform.rotate(self.image, self.angle)
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)

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
            else:
                if hasattr(target, 'health'):
                    target.get_damage(self.damage)
                    # self.get_damage(target.damage)
                else:
                    target.kill()

            # if target.object_type == 'bullet':
            #     target.kill()
            #     self.kill() # kill bullet when bullet bump

    def get_damage(self, value):
        self.health -= value
        if self.health <= 0:
            self.kill()

    def no_move(self):
        self.direction.x = 0
        self.direction.y = 0

    def object_movement_collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite == self:
                pass
            elif sprite == self.user:
                # keep bullet hit self
                pass
            elif sprite.object_type == 'entity':
                if sprite.rect.colliderect(self.rect):
                    self.touch_target(sprite)
            elif sprite.object_type == 'bullet':
                if sprite.rect.colliderect(self.rect):
                    if sprite.user != self.user:
                        if sprite.direction.magnitude() != 0:
                            self.touch_target(sprite)
            elif not self.across_wall:
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

    def out_border(self):
        if self.rect.y < -100 and self.direction.y < 0:
            self.rect.y = map_height
        elif self.rect.y > map_height + 100:
            self.rect.y -= 1000
        if self.rect.x < -200:
            self.rect.x = map_width
        elif self.rect.x > map_width + 200:
            self.rect.x = 0

    def update(self):
        self.move()
        self.out_border()