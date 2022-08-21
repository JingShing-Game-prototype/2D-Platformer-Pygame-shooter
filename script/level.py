import pygame
from tiles import Tile
from player import Player
from settings import tile_size
from particles import ParticleEffect
from bullet import Bullet
from weapon import Weapon
from enemy import Enemy
import math
from debug import debug

class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.display_surface = surface
        self.level_data = level_data

        self.world_shift = pygame.math.Vector2(0, 0)
        self.current_x = 0
        
        # sprite group
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.tiles = pygame.sprite.Group()
        # single group for single player
        self.player = pygame.sprite.GroupSingle()
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.bullet_sprite = pygame.sprite.Group()
        self.enemy_sprite = pygame.sprite.Group()

        # dust
        self.player_on_ground = False
        self.setup_level(self.level_data)

        # bullet
        self.max_bullet_in_map = 100
        self.bullet_far_kill_range = 800

    def create_jump_or_run_particles(self, pos, type='run'):
        if not self.player.sprite.flip:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos -= pygame.math.Vector2(-10, 5)
        ParticleEffect(pos, [self.visible_sprites, self.dust_sprite], type)

    def create_bullet(self, pos=pygame.math.Vector2(), type=None, direction=pygame.math.Vector2(0, 0), speed = 0.1, user=None, across_wall=False):
        if user:
            if not user.flip:
                pos -= pygame.math.Vector2(10, 5)
            else:
                pos -= pygame.math.Vector2(-10, 5)
        if type:
            Bullet(pos, [self.visible_sprites, 
                        self.bullet_sprite,
                        self.obstacle_sprites], 
                        self.obstacle_sprites,
                        type, 
                        direction,
                        speed,
                        self.create_blood_effect,
                        user,
                        across_wall)
        else:
            Bullet(pos, [self.visible_sprites, 
                        self.bullet_sprite,
                        self.obstacle_sprites], 
                        self.obstacle_sprites,
                        direction = direction,
                        speed = speed,
                        create_blood_effect = self.create_blood_effect,
                        user=user,
                        across_wall=across_wall)

    def create_blood_effect(self, pos, type='blood'):
        ParticleEffect(pos, [self.visible_sprites, self.dust_sprite], type)

    def less_bullet(self, amount = 50):
        if len(self.bullet_sprite.sprites())>amount:
            for sprite in self.bullet_sprite.sprites():
                if len(self.bullet_sprite.sprites())<=amount:
                    break
                sprite.kill()

    def far_bullets_kill(self, amount = 50):
        if len(self.bullet_sprite.sprites())>amount:
            for sprite in self.bullet_sprite.sprites():
                if len(self.bullet_sprite.sprites())<=amount:
                    break
                if math.sqrt((sprite.rect.x - self.player.sprite.rect.x)**2 + (sprite.rect.y - self.player.sprite.rect.y)**2) > self.bullet_far_kill_range:
                    sprite.kill()

    def stop_bullets_kill(self, amount = 10):
        if len(self.bullet_sprite.sprites())>amount:
            for sprite in self.bullet_sprite.sprites():
                if len(self.bullet_sprite.sprites())<=amount:
                    break
                if sprite.direction.magnitude() == 0:
                    sprite.kill()

    def get_player_on_ground(self):
        if self.player.sprite:
            self.player_on_ground = True if self.player.sprite.on_ground else False

    def create_landing_dust(self):
        if self.player.sprite:
            if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
                offset = pygame.math.Vector2(10, 15) if not self.player.sprite.flip else pygame.math.Vector2(-10, 15)
                ParticleEffect(self.player.sprite.rect.midbottom - offset, 
                [self.visible_sprites, 
                self.dust_sprite],
                'landing')

    def setup_level(self, layout, reset = False):
        if reset:            
            self.visible_sprites.empty()
            self.obstacle_sprites.empty()
            self.tiles.empty()
            self.player.empty()
            self.dust_sprite.empty()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    Tile((x, y), 
                    [self.visible_sprites,
                    self.tiles,
                    self.obstacle_sprites
                    ], 
                    tile_size)
                elif cell == 'P':
                    if self.player.sprite and not reset:
                        self.player.sprite.rect.x = x
                        self.player.sprite.rect.y = y
                    else:
                        Player((x, y), 
                        [self.visible_sprites,
                        self.obstacle_sprites, 
                        self.player], 
                        self.obstacle_sprites,
                        self.create_jump_or_run_particles,
                        self.create_bullet,
                        self.create_weapon)
            
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                # enemy need player as target
                # enemy might spawn before player spawn
                if cell == 'N':
                    Enemy((x, y), 
                    [self.visible_sprites,
                    self.obstacle_sprites, 
                    self.enemy_sprite], 
                    self.obstacle_sprites,
                    self.create_jump_or_run_particles,
                    self.create_bullet,
                    self.player.sprite,
                    self.create_weapon)

    def create_weapon(self, user, type=None, target=None):
        if type:
            return Weapon([self.visible_sprites],
                            self.obstacle_sprites,
                            user, 
                            self.player.sprite,
                            type = type,
                            create_blood_effect = self.create_blood_effect)
        else:
            return Weapon([self.visible_sprites],
                            self.obstacle_sprites,
                            user, 
                            self.player.sprite,
                            create_blood_effect = self.create_blood_effect)

    def no_player(self):
        if not self.player.sprite:
            self.setup_level(self.level_data, True) # keep body

    def run(self):
        # self.less_bullet()
        self.no_player()
        self.less_bullet(self.max_bullet_in_map)
        self.stop_bullets_kill(10)
        # self.far_bullets_kill(10)
        if self.player.sprite:
            self.visible_sprites.custom_draw(self.player.sprite)
        else:
            self.visible_sprites.custom_draw(self.enemy_sprite.sprites()[0])
        self.visible_sprites.update()
        self.get_player_on_ground()
        self.create_landing_dust()

        if self.player.sprite:
            debug(str(self.player.sprite.rect))
            debug(str(pygame.mouse.get_pos()), 10, 30)
            debug(str(self.player.sprite.health), 10, 50)
            debug(str(len(self.bullet_sprite)), 10, 70)

from settings import screen, screen_height, screen_width
class YSortCameraGroup(pygame.sprite.Group):
    # in godot we call it YSort to make 2.5D
    def __init__(self):
        # general setup
        super().__init__()

        # camera offset
        self.offset = pygame.math.Vector2()
        # to stay player in middle of screen. cut it half.
        self.half_screen_width = screen.get_size()[0]//2
        self.half_screen_height = screen.get_size()[1]//2
        # //2 to get divide 2 result in int

        # box camera setup
        # self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
        self.camera_borders = {'left': 400, 'right': 200, 'top': 200, 'bottom': 200}
        camera_boarders_left = self.camera_borders['left']
        camera_boarders_top = self.camera_borders['top']
        camera_boarders_width = screen.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        camera_boarders_height = screen.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(camera_boarders_left, camera_boarders_top, camera_boarders_width, camera_boarders_height)

        # camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 0.4

        # zoom
        self.zoom_scale = 1
        # don't set too large would be lag
        self.internal_surface_size = (screen_width * 1.5, screen_height * 1.5)
        self.internal_surface = pygame.Surface(self.internal_surface_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surface.get_rect(center = (self.half_screen_width, self.half_screen_height))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surface_size)
        self.internal_offset = pygame.math.Vector2() # need to add after all offset: ground and every object
        self.internal_offset.x = self.internal_surface_size[0] // 2 - self.half_screen_width
        self.internal_offset.y = self.internal_surface_size[1] // 2 - self.half_screen_height

        self.zoom_scale_mininum = screen_width/self.internal_surface_size[0] # change to large scale
        # self.zoom_scale_maxinum = self.internal_surface_size[0]/screen_width
        # self.zoom_scale_mininum = 0.1 # change to large scale
        self.zoom_scale_maxinum = 5

        self.mouse_camera = False
        self.test_camera_box = False

    def center_target_camera(self, target):
        # put target at camera center
        # self.offset.x = player.rect.centerx - self.half_screen_width
        # self.offset.y = player.rect.centery - self.half_screen_height
        self.offset.x = target.rect.centerx - self.half_screen_width
        self.offset.y = target.rect.centery - self.half_screen_height

    def box_target_camera(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def keyboard_control_camera(self):
        keys = pygame.key.get_pressed()
        # ver 1 only for keyboard
        # if keys[pygame.K_a]:self.offset.x -= self.keyboard_speed
        # if keys[pygame.K_d]:self.offset.x += self.keyboard_speed
        # if keys[pygame.K_w]:self.offset.y -= self.keyboard_speed
        # if keys[pygame.K_s]:self.offset.y += self.keyboard_speed
            
        # ver 2 for keyboard and camera box
        if keys[pygame.K_t]:self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_y]:self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_g]:self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_h]:self.camera_rect.y += self.keyboard_speed
        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def mouse_control_camera(self):
        # mouse setting
        # pygame.event.set_grab(True) # make mouse can't leave screen anymore
        if pygame.mouse.get_focused():
            mouse = pygame.math.Vector2(pygame.mouse.get_pos())
            mouse_offset_vector = pygame.math.Vector2()

            left_border = self.camera_borders['left']
            top_border = self.camera_borders['top']
            right_border = screen.get_size()[0] - self.camera_borders['right']
            bottom_border = screen.get_size()[1] - self.camera_borders['bottom']

            if top_border < mouse.y < bottom_border:
                if mouse.x < left_border:
                    mouse_offset_vector.x = mouse.x - left_border
                    # pygame.mouse.set_pos((left_border, mouse.y))
                if mouse.x > right_border:
                    mouse_offset_vector.x = mouse.x - right_border
                    # pygame.mouse.set_pos((right_border, mouse.y))
            elif mouse.y < top_border:
                if mouse.x < left_border:
                    mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
                    # pygame.mouse.set_pos((left_border, top_border))
                if mouse.x > right_border:
                    mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
                    # pygame.mouse.set_pos((right_border, top_border))
            elif mouse.y > bottom_border:
                if mouse.x < left_border:
                    mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
                    # pygame.mouse.set_pos((left_border, bottom_border))
                if mouse.x > right_border:
                    mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)
                    # pygame.mouse.set_pos((right_border, bottom_border))

            if left_border < mouse.x < right_border:
                if mouse.y < top_border:
                    mouse_offset_vector.y = mouse.y - top_border
                    # pygame.mouse.set_pos((mouse.x, top_border))
                if mouse.y > bottom_border:
                    mouse_offset_vector.y = mouse.y - bottom_border
                    # pygame.mouse.set_pos((mouse.x, bottom_border))

            # self.offset += mouse_offset_vector * self.mouse_speed # ver 1 for only mouse
            self.camera_rect.x += mouse_offset_vector.x * self.mouse_speed
            self.camera_rect.y += mouse_offset_vector.y * self.mouse_speed

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_EQUALS]:
            self.zoom_scale += 0.1
        if keys[pygame.K_MINUS]:
            self.zoom_scale -= 0.1
        if keys[pygame.K_9]:
            self.zoom_scale = 1

    def custom_draw(self, player):
        # getting the offset
        # self.center_target_camera(player) # center camera
        self.box_target_camera(player) # camera box
        self.keyboard_control_camera()
        self.zoom_keyboard_control()
        if self.mouse_camera:
            self.mouse_control_camera()

        # limit scale size
        if self.zoom_scale < self.zoom_scale_mininum:
            self.zoom_scale = self.zoom_scale_mininum
        elif self.zoom_scale > self.zoom_scale_maxinum:
            self.zoom_scale = self.zoom_scale_maxinum
        
        self.internal_surface.fill('grey')

        # drawing the floor
        # offset needed
        # floor_offset_pos = self.floor_rect.topleft - self.offset + self.internal_offset
        # self.internal_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            # use sort to create the YSort. and now it has overlap.
            # for camera sprite.rect need to add a offset. 
            # and offset comes from player
            # offset needed
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            # to make camera direction right need to subtract offset
            # screen.blit(sprite.image, offset_pos)
            if hasattr(sprite, 'object_type'):
                if sprite.object_type == 'player':
                    sprite.offset_pos = offset_pos
            self.internal_surface.blit(sprite.image, offset_pos)

        scaled_surf  = pygame.transform.scale(self.internal_surface, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.half_screen_width, self.half_screen_height))

        screen.blit(scaled_surf, scaled_rect)
        
        if self.test_camera_box:
            # camera box line
            pygame.draw.rect(screen, 'yellow', self.camera_rect, 5)