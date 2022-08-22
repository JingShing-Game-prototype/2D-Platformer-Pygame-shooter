from crt_shader import Graphic_engine
import pygame, os, sys

def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		absolute_path = os.path.join(sys._MEIPASS, relative)
	else:
		absolute_path = os.path.join(relative)
	return absolute_path

pygame.init()

def get_map_width_and_height(map, tile_size):
	map_width = len(map[0])*tile_size
	map_height = len(map) * tile_size
	return map_width, map_height


no_enemy_level_map = [
'                            ',
'                            ',
'                            ',
' XX    XXX            XX    ',
' XX P                       ',
' XXXX         XX         XX ',
' XXXX       XX              ',
' XX    X  XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

level_map = [
'                            ',
'                            ',
'                       N    ',
' XX    XXX            XX    ',
' XX P         N             ',
' XXXX         XX         XX ',
' XXXX      NXX              ',
' XX    X  XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

tile_size = 64
screen_width = 64*15
screen_height = 640
map_width, map_height = get_map_width_and_height(level_map, tile_size)

VIRTUAL_RES = (screen_width, screen_height)
REAL_RES = (1280, 720)
# VIRTUAL_RES = (800, 600)
# REAL_RES = (800, 600)
pygame.display.set_mode(REAL_RES, pygame.DOUBLEBUF|pygame.OPENGL)

# game icon
pygame.display.set_icon(pygame.image.load(resource_path('assets\icon\icon.png')).convert_alpha())
pygame.display.set_caption('Gun Fight')

screen = pygame.Surface(VIRTUAL_RES).convert((255, 65280, 16711680, 0))
crt_shader = Graphic_engine(screen=screen, style=2, VIRTUAL_RES=VIRTUAL_RES)

weapon_bullet_type = {
	'ak74':{'name':'bullet', 'across_wall':False},
	'bullet':{'name':'ak74', 'across_wall':False},
	'sword':{'name':'sword', 'across_wall':True},
}

weapon_data = {
	'ak74':{'size':(96, 32)},
	'bullet':{'size':(32, 16)},
	'sword':{'size':(120, 30), 'melee_angle_speed':10, 'melee_attack_cd':5, 'melee_attack_direction':1},
	'shield':{'size':(120, 120)},
}

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = None
UI_FONT_SIZE = 30
 
# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
 
# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
STAMINA_COLOR = 'green'
UI_BORDER_COLOR_ACTIVE = 'gold'

# upgrade menu
TEXT_COLOR_SELECTED = '#111111'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#111111'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'