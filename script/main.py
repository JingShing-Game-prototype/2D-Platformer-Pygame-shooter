import pygame, sys
from settings import *
from level import Level

# pygame setup
pygame.init()
pygame.display.set_icon(pygame.image.load(resource_path('assets\icon\icon.png')).convert_alpha())
pygame.display.set_caption('Gun Fight')
clock = pygame.time.Clock()
level = Level(level_data=no_enemy_level_map, surface=screen)

def dynamic_bullet_amount():
    if clock.get_fps() < 40 and level.max_bullet_in_map > 100:
        level.max_bullet_in_map -= 10
    else:
        level.max_bullet_in_map = 300

while True:
    for event in pygame.event.get():
        pygame.display.set_caption('Gun Fight' + ' : ' + str(round(clock.get_fps(), 1)))
        dynamic_bullet_amount()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                crt_shader.change_shader()
            if event.key == pygame.K_8:
                crt_shader.fullscreen = not crt_shader.fullscreen
                crt_shader.Full_screen(REAL_RES)
            if event.key == pygame.K_r:
                level.setup_level(level.level_data, True)
            if event.key == pygame.K_m:
                level.visible_sprites.mouse_camera = not level.visible_sprites.mouse_camera
            if event.key == pygame.K_l:
                level.visible_sprites.test_camera_box = not level.visible_sprites.test_camera_box
            if event.key == pygame.K_o:
                for sprite in level.enemy_sprite.sprites():
                    sprite.defense = not sprite.defense
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1:
        #         if level.player.sprite:
        #             level.player.sprite.bullet_shoot(mode='mouse')
                # only scroll can shoot
                # 1 - left click
                # 2 - middle click
                # 3 - right click
                # 4 - scroll up
                # 5 - scroll down

    level.run()
    
    crt_shader()
    clock.tick(60)