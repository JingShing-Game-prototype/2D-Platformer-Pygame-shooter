from object import Object
import pygame

class Flesh(Object):
    def __init__(self, pos, groups, obstacle_sprites, type='flesh', id=0, exist_duration=-1,  direction=pygame.math.Vector2(), speed=5):
        super().__init__(groups)
        self.or_image = pygame.surface.Surface((32, 16))
        self.or_image.fill((200, 0, 0))
        self.image = self.or_image.copy()
        self.type = type
        self.item_id = id
        self.rect = self.image.get_rect(topleft = pos)
        self.obstacle_sprites = obstacle_sprites
        self.exsist_time = pygame.time.get_ticks()
        self.exsist_duration = exist_duration
        self.speed = speed
        self.direction = direction

    def update(self):
        self.move()
        if self.direction.magnitude() != 0:
            self.adjust_pos()
        self.stop_on_ground()
        self.common_cooldown()