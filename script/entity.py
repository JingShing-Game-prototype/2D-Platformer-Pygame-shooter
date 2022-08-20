import pygame
from random import randint

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.object_type = None
        self.frame_index = 0
        self.animation_speed = 0.15

        # status
        self.health = 100
        self.status = 'idle'
        self.crouch = False
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

        # bullet
        self.aim_rate = 20
        self.using_weapon = False
        self.using_weapon_time = None
        self.using_weapon_cd = 50
        # bullet speed 100 is like real
        self.bullet_speed = 10
        self.can_shoot = True
        self.shoot_time = None
        self.shoot_cooldown = 100
        self.shoot_times = 1
        self.shoot_se = pygame.mixer.Sound('assets\\audio\SE\Gunshot_SE.mp3')
        self.shoot_se.set_volume(0.01)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            # self.dust_frame_index += self.dust_animation_speed
            # if self.dust_frame_index >= len(self.dust_run_particles):
            #     self.dust_frame_index = 0
            # dust_particle = self.dust_run_particles[int(self.dust_frame_index)] if not self.flip else pygame.transform.flip(self.dust_run_particles[int(self.dust_frame_index)], True, False)
            # pos = self.rect.bottomleft - pygame.math.Vector2(6, 10) if not self.flip else self.rect.bottomright - pygame.math.Vector2(6, 10)
            self.create_jump_or_run_particles(self.rect.midbottom, 'run')

    def bullet_shoot(self, mode='key'):
        if self.object_type == 'player':
            if self.can_shoot:
                self.shoot_se.play()
                self.using_weapon = True
                self.using_weapon_time = pygame.time.get_ticks()
                if mode == 'mouse':
                    mouse_pos = pygame.mouse.get_pos()
                    # to make mouse accurate
                    user_pos = self.offset_pos
                    x = mouse_pos[0] - user_pos[0]
                    y = mouse_pos[1] - user_pos[1]
                    if x < 0:
                        self.flip = True
                    else:
                        self.flip = False
                    
                    # gun shot point pos
                    pos = self.weapon.gun_shot_pos

                    for i in range(self.shoot_times):
                        direction = pygame.math.Vector2(x, y + randint(-self.aim_rate, self.aim_rate))
                        self.create_bullet(pos=pos, direction = direction, speed = self.bullet_speed)

                elif mode == 'key':
                    if not self.flip:
                        pos = self.rect.midright + pygame.math.Vector2(10, 0)
                        direction = pygame.math.Vector2(1, 0)
                    else:
                        pos = self.rect.midleft + pygame.math.Vector2(-10, 0)
                        direction = pygame.math.Vector2(-1, 0)
                    self.create_bullet(pos=pos, direction = direction, speed = self.bullet_speed)

                self.shoot_time = pygame.time.get_ticks()
                self.can_shoot = False
                # self.using_weapon = False
        elif self.object_type == 'enemy':
            if self.can_shoot and self.weapon:
                self.shoot_se.play()
                self.using_weapon = True
                target_pos = self.target.rect
                user_pos = self.rect
                x = target_pos[0] - user_pos[0]
                y = target_pos[1] - user_pos[1]
                if x < 0:
                    self.flip = True
                else:
                    self.flip = False

                pos = self.weapon.gun_shot_pos
                    
                for i in range(self.shoot_times):
                    direction = pygame.math.Vector2(x, y + randint(-self.aim_rate, self.aim_rate))
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
        if self.using_weapon:
            if now - self.using_weapon_time > self.using_weapon_cd:
                self.using_weapon = False

    def get_damage(self, value):
        self.health -= value
        if self.health <= 0:
            self.kill()
            self.weapon.kill()
