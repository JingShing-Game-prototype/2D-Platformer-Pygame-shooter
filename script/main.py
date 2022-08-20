import pygame, sys
from settings import *
from level import Level

# pygame setup
pygame.init()
clock = pygame.time.Clock()
level = Level(level_data=level_map, surface=screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                crt_shader.change_shader()
            if event.key == pygame.K_r:
                level.setup_level(level.level_data, True)
            if event.key == pygame.K_m:
                level.visible_sprites.mouse_camera = not level.visible_sprites.mouse_camera
            if event.key == pygame.K_l:
                level.visible_sprites.test_camera_box = not level.visible_sprites.test_camera_box
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 4 or event.button == 5:
                # only scroll can shoot
                level.player.sprite.bullet_shoot(mode='mouse')
                # 1 - left click
                # 2 - middle click
                # 3 - right click
                # 4 - scroll up
                # 5 - scroll down

    level.run()
    
    crt_shader()
    clock.tick(60)