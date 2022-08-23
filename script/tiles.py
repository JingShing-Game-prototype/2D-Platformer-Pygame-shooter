import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, size):
        super().__init__(groups)
        self.used_groups = groups
        self.object_type = 'tile'
        self.image = pygame.Surface((size, size))
        # self.image.fill('grey')
        self.image.fill((100,100,100))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, shift=pygame.math.Vector2(0,0)):
        self.rect.x += shift.x
        self.rect.y += shift.y