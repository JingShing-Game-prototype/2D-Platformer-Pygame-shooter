import pygame
from random import randint

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type=None):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.5
        self.type = type
        self.pos = pos
        # control blood is green or red
        self.china = False
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
        for i in range(self.frame_length):
            self.frames.append(effect)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=self.pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.type == 'blood':
            self.rect = self.image.get_rect(center=self.pos + pygame.math.Vector2(randint(-5, 5), randint(-10, 10)))
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, shift=pygame.math.Vector2(0,0)):
        self.animate()
        self.rect.x += shift.x
        self.rect.y += shift.y