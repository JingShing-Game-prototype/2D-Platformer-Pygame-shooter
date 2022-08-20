from crt_shader import Graphic_engine
import pygame, os, sys

def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		absolute_path = os.path.join(sys._MEIPASS, relative)
	else:
		absolute_path = os.path.join(relative)
	return absolute_path

pygame.init()

level_map = [
'                            ',
'                            ',
'                       N    ',
' XX    XXX            XX    ',
' XX P         N             ',
' XXXX         XX         XX ',
' XXXX       XX              ',
' XX    X  XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

tile_size = 64
# screen_width = 1200
# screen_height = len(level_map) * tile_size
screen_width = 64*15
screen_height = 640

VIRTUAL_RES = (screen_width, screen_height)
REAL_RES = (1280, 720)
# VIRTUAL_RES = (800, 600)
# REAL_RES = (800, 600)
pygame.display.set_mode(REAL_RES, pygame.DOUBLEBUF|pygame.OPENGL)
screen = pygame.Surface(VIRTUAL_RES).convert((255, 65280, 16711680, 0))
crt_shader = Graphic_engine(screen=screen, style=2, VIRTUAL_RES=VIRTUAL_RES)