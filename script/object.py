import pygame
import numpy
from random import randint
from settings import map_width, map_height

# for item or particles
class Object(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.object_type = 'object'
        self.type = None
        self.item_id = 0
        self.frame_index = 0
        self.animation_speed = 0.15

        # status
        self.exsist_time = None
        self.exsist_duration = -1
        self.status = 'idle'
        self.flip = False
        # not flip is right
        # flip is left
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.or_speed = 8
        self.speed = self.or_speed
        self.or_gravity = 0.8
        self.gravity = self.or_gravity
        self.or_jump_speed = -16
        self.jump_speed = self.or_jump_speed

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity+0.1:
            self.status = 'fall'
        else:
            if self.direction.x !=0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def no_move(self):
        self.direction.x = 0
        self.direction.y = 0

    def stop_on_ground(self):
        if self.direction.y <= 0 and self.on_ground:
            self.direction.x = 0

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.apply_gravity()
        self.collision('vertical')
        self.over_border()

    def over_border(self):
        # if out map it's a loop
        if self.rect.y < -100 and self.direction.y < 0:
            self.rect.y = 0
            self.direction.y = 0
        elif self.rect.y > map_height + 200:
            self.rect.y -= 1000
            self.direction.y = 0
        if self.rect.x > map_width + 500:
            self.rect.x = 0
        elif self.rect.x < 0 - 500:
            self.rect.x = map_width

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite == self:
                pass
            elif sprite.object_type == 'entity':
                pass
            else:
                if direction == 'horizontal':
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.x < 0:
                            self.rect.left = sprite.rect.right
                            self.on_left = True
                            self.current_x = self.rect.left
                        if self.direction.x > 0:
                            self.rect.right = sprite.rect.left
                            self.on_right = True
                            self.current_x = self.rect.right

                    if self.on_left and (self.rect.left < self.current_x or self.direction.x >= 0):
                        self.on_left = False
                    if self.on_right and (self.rect.right > self.current_x or self.direction.x <= 0):
                        self.on_right = False

                elif direction == 'vertical':
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.y > 0:
                            self.rect.bottom = sprite.rect.top
                            self.direction.y = 0
                            self.on_ground = True
                        elif self.direction.y < 0:
                            self.rect.top = sprite.rect.bottom
                            self.direction.y = 0
                            self.on_ceiling = True

            if self.on_ground and self.direction.y < 0 or self.direction.y > 1:
                self.on_ground = False
            if self.on_ceiling and self.direction.y > 0.1:
                self.on_ceiling = False

    def common_cooldown(self):
        now = pygame.time.get_ticks()
        if self.exsist_duration > 0:
            if now - self.exsist_time > self.exsist_duration:
                self.kill()

    def adjust_pos(self):
        # get angle rotate and image pos
        x = self.direction.x
        y = self.direction.y
        
        angle = 0
        if x!=0 and y!=0:
            angle = numpy.arctan(y/x) * 180 / 3.14
        elif x==0:
            if y < 0:
                angle = 90
            elif y > 0:
                angle = 270
        else:
            angle = 0
        self.angle = angle
        self.image = pygame.transform.rotate(self.or_image, angle)
