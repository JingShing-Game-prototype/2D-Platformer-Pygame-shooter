import pygame

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, groups, type=None):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.5
        if type == 'run':
            effect = pygame.Surface((32, 32))
            effect.fill('blue')
        else:
            effect = pygame.Surface((32, 16))
            effect.fill('red')
        self.frames = []
        for i in range(5):
            self.frames.append(effect)
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, shift=pygame.math.Vector2(0,0)):
        self.animate()
        self.rect.x += shift.x
        self.rect.y += shift.y