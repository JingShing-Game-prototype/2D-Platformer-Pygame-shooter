import pygame
from settings import screen
pygame.init()
font = pygame.font.Font(None,30)
 
def debug(info, x = 10, y = 10):
    debug_surf = font.render(str(info),True,'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pygame.draw.rect(screen,'Black',debug_rect)
    screen.blit(debug_surf,debug_rect)