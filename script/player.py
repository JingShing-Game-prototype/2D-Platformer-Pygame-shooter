import pygame
from entity import Entity
from settings import joystick

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_jump_or_run_particles, create_bullet, create_weapon, create_flesh):
        super().__init__(groups)
        self.import_character_assets()
        self.type = 'player'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # fix mouse pos wrong
        self.offset_pos = self.rect

        # UI
        self.current_health = self.health
        self.health_bar_length = self.or_health * 2
        self.health_ratio = self.or_health / self.health_bar_length
        self.health_change_speed = 0.15

        # particles
        self.create_jump_or_run_particles = create_jump_or_run_particles
        self.create_bullet = create_bullet
        self.create_flesh = create_flesh
        
        # player movement
        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.can_switch_weapon = True
        self.switch_weapon_time = None
        self.switch_weapon_cd = 500
        self.weapon_index = 2
        self.create_weapon = create_weapon
        self.weapon = self.create_weapon(user=self, type=self.weapon_list[self.weapon_index])

        # input cd
        self.can_input = True
        self.input_time = None
        self.input_cd = 200

        # joystick mode
        self.use_joystick = True
        self.joystick_aim = False
        self.joystick_camera = False

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
            # left click
            self.bullet_shoot()
        if mouse[2]:
            # right click
            self.melee_attack()
        elif keys[pygame.K_e]:
            self.switch_weapon('next')
        elif keys[pygame.K_q]:
            self.switch_weapon('before')

        if not self.joystick_camera:
            if joystick.get_hat(0)[0]==1:
                # dpad right
                self.direction.x = 1
                self.flip = False
            elif joystick.get_hat(0)[0]==-1:
                # dpad left
                self.direction.x = -1
                self.flip = True
            if joystick.get_hat(0)[1]==1:
                # dpad up and A button
                self.gravity = self.or_gravity
                self.jump()
                self.create_jump_or_run_particles(self.rect.midbottom, 'jump')
        if self.can_input:
            self.can_input = False
            self.input_time = pygame.time.get_ticks()
            if joystick.get_button(9):
                self.joystick_aim = not self.joystick_aim
            if joystick.get_button(8):
                self.joystick_camera = not self.joystick_camera
        if joystick.get_axis(0)>=0.5:
            # joystick right
            self.direction.x = 1
            self.flip = False
        elif joystick.get_axis(0)<=-0.5:
            # joystick
            self.direction.x = -1
            self.flip = True
        if (joystick.get_button(0) or joystick.get_axis(1)<=-0.5) and self.on_ground:
            # joystick up and A button
            self.gravity = self.or_gravity
            self.jump()
            self.create_jump_or_run_particles(self.rect.midbottom, 'jump')
        if joystick.get_axis(5) > 0:
            # RT
            self.bullet_shoot()
        if joystick.get_axis(4) > 0.5:
            # LT
            self.melee_attack()
        if joystick.get_button(3):
            # Y button
            self.switch_weapon('before')
        if joystick.get_button(1):
            # B button
            self.switch_weapon('next')

        # joystick
        # A Button        - Button 0
        # B Button        - Button 1
        # X Button        - Button 2
        # Y Button        - Button 3
        # Left Bumper     - Button 4
        # Right Bumper    - Button 5
        # Back Button     - Button 6
        # Start Button    - Button 7
        # L. Stick In     - Button 8
        # R. Stick In     - Button 9
        # Guide Button    - Button 10

        # Axis 0 -> left joystick x
        # Axis 1 -> left joystick y
        # Axis 2 -> right joystick x
        # Axis 3 -> right joystick y
        # Axis 4 -> LT
        # Axis 5 -> RT

        # dpad Hat 0 value(0, 0)

    def switch_weapon(self, which='next'):
        if self.weapon and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.switch_weapon_time = pygame.time.get_ticks()
            if which == 'next':
                self.weapon_index = (self.weapon_index + 1) % len(self.weapon_list)
            elif which == 'before':
                self.weapon_index = (self.weapon_index + len(self.weapon_list) - 1) % len(self.weapon_list)
            self.weapon_type = self.weapon_list[self.weapon_index]
            self.weapon.__init__(user=self.weapon.user, obstacle_sprite = self.weapon.obstacle_sprite, groups=self.weapon.sprite_groups, target=self.weapon.target, type=self.weapon_list[self.weapon_index], create_blood_effect=self.weapon.create_blood_effect)

    def cooldown(self):
        now = pygame.time.get_ticks()
        if not self.can_switch_weapon:
            if now - self.switch_weapon_time > self.switch_weapon_cd:
                self.can_switch_weapon = True
        if not self.can_input:
            if now - self.input_time > self.input_cd:
                self.can_input = True

    def update(self):
        # self.debug_show_can_jump()
        self.common_cooldown()
        self.cooldown()
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        self.move()