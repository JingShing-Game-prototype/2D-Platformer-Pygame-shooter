import pygame
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, creat_jump_or_run_particles, create_bullet):
        super().__init__(groups)
        self.import_character_assets()
        self.object_type = 'player'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        # self.image = pygame.Surface((32, 64))
        # self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)

        # fix mouse pos wrong
        self.offset_pos = self.rect

        # particles
        self.creat_jump_or_run_particles = creat_jump_or_run_particles
        self.create_bullet = create_bullet
        
        # player movement
        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2(0, 0)
        self.or_speed = 8
        self.speed = self.or_speed
        self.or_gravity = 0.8
        self.gravity = self.or_gravity
        self.or_jump_speed = -16
        self.jump_speed = self.or_jump_speed

        # player status
        self.status = 'idle'
        self.flip = False
        # not flip is right
        # flip is left
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        # bullet
        self.using_weapon = False
        self.bullet_speed = 10
        self.can_shoot = True
        self.shoot_time = None
        self.shoot_cooldown = 50
        self.shoot_times = 1

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

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            # self.dust_frame_index += self.dust_animation_speed
            # if self.dust_frame_index >= len(self.dust_run_particles):
            #     self.dust_frame_index = 0
            # dust_particle = self.dust_run_particles[int(self.dust_frame_index)] if not self.flip else pygame.transform.flip(self.dust_run_particles[int(self.dust_frame_index)], True, False)
            # pos = self.rect.bottomleft - pygame.math.Vector2(6, 10) if not self.flip else self.rect.bottomright - pygame.math.Vector2(6, 10)
            self.creat_jump_or_run_particles(self.rect.midbottom, 'run')

    def get_input(self):
        keys = pygame.key.get_pressed()
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
            self.creat_jump_or_run_particles(self.rect.midbottom)

        if keys[pygame.K_f] and self.can_shoot:
            self.shoot_time = pygame.time.get_ticks()
            self.can_shoot = False
            if not self.flip:
                pos = self.rect.midright + pygame.math.Vector2(10, 0)
                direction = pygame.math.Vector2(1, 0)
            else:
                pos = self.rect.midleft + pygame.math.Vector2(-10, 0)
                direction = pygame.math.Vector2(-1, 0)
            self.create_bullet(pos=pos, direction = direction, speed = self.bullet_speed)

    def mouse_shoot(self):
        if self.can_shoot:
            self.using_weapon = True
            mouse_pos = pygame.mouse.get_pos()
            user_pos = self.offset_pos
            x = mouse_pos[0] - user_pos[0]
            y = mouse_pos[1] - user_pos[1]
            if x < 0:
                self.flip = True
            else:
                self.flip = False
            if not self.flip:
                pos = self.rect.midright + pygame.math.Vector2(10, 0)
            else:
                pos = self.rect.midleft + pygame.math.Vector2(-10, 0)
            for i in range(self.shoot_times):
                direction = pygame.math.Vector2(x, y + randint(-200, 200))
                self.create_bullet(pos=pos, direction = direction, speed = self.bullet_speed)
        self.shoot_time = pygame.time.get_ticks()
        self.can_shoot = False
        self.using_weapon = False

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

    def debug_show_can_jump(self):
        if self.on_ground:
            self.image.fill('green')
        else:
            self.image.fill('red')

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.apply_gravity()
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if sprite == self:
                pass
            elif sprite.object_type == 'bullet':
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

    def cooldown(self):
        now = pygame.time.get_ticks()
        if not self.can_shoot:
            if now - self.shoot_time > self.shoot_cooldown:
                self.can_shoot = True

    def update(self):
        # self.debug_show_can_jump()
        self.cooldown()
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.move()