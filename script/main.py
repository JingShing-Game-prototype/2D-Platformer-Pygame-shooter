import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        # pygame setup
        pygame.init()
        pygame.mouse.set_visible(False)

        # cursor
        self.cursor_image = pygame.image.load(resource_path('assets/graphics/UI/aim.png'))
        self.cursor_image = pygame.transform.scale(self.cursor_image, (64, 64))
        self.cursor_image_rect = self.cursor_image.get_rect()

        self.clock = pygame.time.Clock()
        # self.level = Level(level_data=no_enemy_level_map, surface=screen)
        self.level = Level(level_data=level_map, surface=screen)

    def dynamic_bullet_amount(self):
        if self.clock.get_fps() < 40 and self.level.max_bullet_in_map > 100:
            self.level.max_bullet_in_map -= 10
        else:
            self.level.max_bullet_in_map = 300

    def run(self):
        while True:
            for event in pygame.event.get():
                pygame.display.set_caption('Gun Fight' + ' : ' + str(round(self.clock.get_fps(), 1)))
                self.dynamic_bullet_amount()
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
                        self.level.setup_level(self.level.level_data, True)
                    if event.key == pygame.K_m:
                        self.level.visible_sprites.mouse_camera = not self.level.visible_sprites.mouse_camera
                    if event.key == pygame.K_l:
                        self.level.visible_sprites.test_camera_box = not self.level.visible_sprites.test_camera_box
                    if event.key == pygame.K_o:
                        for sprite in self.level.enemy_sprite.sprites():
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

            self.level.run()
            self.cursor_image_rect.center = pygame.mouse.get_pos()
            screen.blit(self.cursor_image, self.cursor_image_rect)
            crt_shader()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()