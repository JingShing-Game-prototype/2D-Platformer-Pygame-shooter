import pygame
from settings import screen_height, screen_width
import numpy

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, type=None, direction=pygame.math.Vector2(0, 0), speed = 0.1):
        super().__init__(groups)
        self.object_type = 'bullet'
        self.obstacle_sprites = obstacle_sprites
        self.direction = direction
        # self.or_image = pygame.Surface((32, 16))
        # self.or_image.fill((0, 128, 0))
        self.flip = True if self.direction.x < 0 else False
        self.angle = self.adjust_angle()
        self.image = pygame.image.load('assets\graphics\weapon\\bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 16))
        self.image = pygame.transform.rotate(self.image, self.angle)
        if self.flip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def adjust_angle(self):
        x = self.direction.x
        y = self.direction.y
        if x!=0 and y!=0:
            angle = (numpy.arctan(y/x) * 180 / 3.14)
            if not self.flip:
                angle = -angle
        else:
            angle = 0

        return angle

    def object_movement_collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite == self:
                pass
            elif sprite.object_type == 'player':
                pass
            elif sprite.object_type == 'bullet':
                pass
            else:
                if direction == 'horizontal':
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.x < 0:
                            self.rect.left = sprite.rect.right
                            self.direction.x = 0
                            self.direction.y = 0
                        if self.direction.x > 0:
                            self.rect.right = sprite.rect.left
                            self.direction.x = 0
                            self.direction.y = 0
                elif direction == 'vertical':
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.y > 0:
                            self.rect.bottom = sprite.rect.top
                            self.direction.y = 0
                            self.direction.x = 0
                        elif self.direction.y < 0:
                            self.rect.top = sprite.rect.bottom
                            self.direction.y = 0
                            self.direction.x = 0

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