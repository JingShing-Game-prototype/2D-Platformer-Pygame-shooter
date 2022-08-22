import pygame
from random import randint

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type=None, move_to_object_pool=None):
        super().__init__(groups)
        self.object_type = 'particle'
        self.move_to_object_pool=move_to_object_pool
        self.used_groups = groups
        self.frame_index = 0
        self.animation_speed = 0.5
        self.type = type
        self.china = False
        self.get_info()
        self.pos = pos
        # control blood is green or red
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=self.pos)

    def old_particles(self, pos, type):
        self.frame_index = 0
        self.type = type
        self.get_info()
        self.pos = pos
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=self.pos)

    def get_info(self):
        if self.type == 'run':
            effect = pygame.Surface((32, 32))
            effect.fill('blue')
            self.frame_length = 5
        elif self.type == 'jump':
            effect = pygame.Surface((32, 16))
            effect.fill((0, 128, 0))
            self.frame_length = 5
        elif self.type == 'landing':
            effect = pygame.Surface((32, 16))
            effect.fill('green')
            self.frame_length = 5
        elif self.type == 'blood':
            effect = pygame.Surface((8, 8))
            # blood color
            if self.china:
                blood_color = 'green'
            else:
                blood_color = 'red'
            effect.fill(blood_color)
            self.frame_length = 7
        else:
            effect = pygame.Surface((32, 16))
            effect.fill('green')
            self.frame_length = 5
        self.frames = []
        for _ in range(self.frame_length):
            self.frames.append(effect)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.type == 'blood':
            self.rect = self.image.get_rect(center=self.pos + pygame.math.Vector2(randint(-5, 5), randint(-10, 10)))
        if self.frame_index >= len(self.frames):
            self.move_to_object_pool(self)
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, shift=pygame.math.Vector2(0,0)):
        self.animate()
        self.rect.x += shift.x
        self.rect.y += shift.y