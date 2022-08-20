import pygame
from random import randint
from entity import Entity
from settings import screen_width

class Enemy(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_jump_or_run_particles, create_bullet, target, create_weapon):
        super().__init__(groups)
        self.object_type = 'enemy'
        self.or_image = pygame.Surface((32, 64))
        self.or_image.fill((100, 0, 0))
        self.image = self.or_image.copy()
        self.rect = self.image.get_rect(topleft = pos)

        self.target = target

        # particles
        self.create_jump_or_run_particles = create_jump_or_run_particles
        self.create_bullet = create_bullet
        
        # movement
        self.obstacle_sprites = obstacle_sprites

        # bullet
        self.defense = False
        self.create_weapon = create_weapon
        self.weapon = self.create_weapon(user=self, target=self.target)

    def animate(self):
        self.image = self.or_image.copy() if not self.flip else pygame.transform.flip(self.image, True, False)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def AI_attack(self):
        if self.defense:
            self.bullet_shoot()

    def target_distance_and_direction(self, target):
        # get player to enemy distance and direction
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(target.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        # converting vector to distance
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
            # converting vector to unit vector
        else:
            direction = pygame.math.Vector2()
            # vector(0, 0)
        return (distance, direction)

    def AI_move(self):
        distance, direction = self.target_distance_and_direction(self.target)
        if distance < 500 and self.target.using_weapon:
            self.defense = True
        # elif distance > 500 and not(self.target.using_weapon):
        #     self.defense = False
        if self.defense and distance > 100:
            self.direction.x = direction.x
            if self.on_ground:
                self.jump()
                # self.direction.y = direction.y * 2 + self.gravity
        else:
            self.direction.x = 0

        # if out window then kill
        if self.rect.centery > screen_width:
            self.direction.y = 0
            self.rect.y -= 1000
        # if not self.on_ground:
        #     self.jump()

    def update(self):
        self.cooldown()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.AI_move()
        self.AI_attack()
        self.move()