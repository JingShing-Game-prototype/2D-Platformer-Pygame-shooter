import pygame
from random import randint
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_jump_or_run_particles, create_bullet, create_weapon):
        super().__init__(groups)
        self.import_character_assets()
        self.object_type = 'player'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # fix mouse pos wrong
        self.offset_pos = self.rect

        # particles
        self.create_jump_or_run_particles = create_jump_or_run_particles
        self.create_bullet = create_bullet
        
        # player movement
        self.obstacle_sprites = obstacle_sprites

        # bullet
        self.create_weapon = create_weapon
        self.weapon = self.create_weapon(user=self, type='bullet')

    def import_character_assets(self):
        self.animations = {
            'idle':[],
            'run':[],
            'jump':[],
            'fall':[],
        }
        for index, animation in enumerate(self.animations.keys()):
            image = pygame.Surface((32, 64))
            value_r = (index*30)%255
            value_g = (index*60)%255
            value_b = (index*90)%255
            image.fill((value_r, value_g, value_b))
            self.animations[animation].append(image)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)] if not self.flip else pygame.transform.flip(animation[int(self.frame_index)], True, False)

        # set rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center = self.rect.center)

    def get_input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        # left, middle, right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.flip = False
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.flip = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.gravity = self.or_gravity
            self.jump()
            self.create_jump_or_run_particles(self.rect.midbottom, 'jump')

        if keys[pygame.K_f] or mouse[0]:
            self.bullet_shoot(mode='mouse')

    def update(self):
        # self.debug_show_can_jump()
        self.cooldown()
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.move()