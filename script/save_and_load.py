import json
from settings import *

def resource_path(relative):
	if hasattr(sys, "_MEIPASS"):
		absolute_path = os.path.join(sys._MEIPASS, relative)
	else:
		absolute_path = os.path.join(relative)
	return absolute_path


def list_save_map(path, map):
    if path:
        with open(path, 'w', encoding='UTF-8') as save_file:
            json.dump(map, save_file)

def save_map(path, map):
    if path:
        with open(path, 'w', encoding='UTF-8') as file:
            for line in map:
                file.write(line + '\n')

def list_load_map(path):
    if path:
        # read all
        with open(resource_path(path), encoding='UTF-8') as save_file:
            map = json.load(save_file)
            return map

def load_map(path, map):
    if path:
        map.clear()
        # read line by line
        with open(resource_path(path), encoding='UTF-8') as file:
            while(1):
                line = file.readline()
                if not(line):break
                elif line == '\n' or line == '':continue
                else:
                    line = line.replace('\n', '')
                    map.append(line)

import os
def found_save_or_not(level):
    # check if save_file.txt exist
    try:
        with open('save_file.txt') as save_file:
            level.has_save = True
    except:
        level.has_save = False

def found_map_or_not(file_name):
    return os.path.exists(resource_path('assets/maps/' + file_name))

def found_asset_imgs(folder_path='assets/graphics/characters/', img_dict=None, transform = False, scale=(152, 152), allow_img_format = ['png', 'jpg', 'bmp']):
    if img_dict:
        if len(img_dict) > 1 and not('none' in img_dict):
            img_dict.clear()
        folder_path = resource_path(folder_path)
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_format = file_name.split('.')[-1]
            if file_format in allow_img_format:
                file_fore_name = file_name.split('.')[0]
                if transform:
                    img_dict[file_fore_name] = pygame.transform.scale(pygame.image.load(folder_path + file_name), scale)
                else:
                    img_dict[file_fore_name] = pygame.image.load(folder_path + file_name)

def found_asset_sounds(folder_path='assets/audio/sound/', sound_dict=None, allow_sound_format = ['mp3', 'wav']):
    if sound_dict:
        sound_dict.clear()
        folder_path = resource_path(folder_path)
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_format = file_name.split('.')[-1]
            if file_format in allow_sound_format:
                file_fore_name = file_name.split('.')[0]
                sound_dict[file_fore_name] = pygame.mixer.Sound(folder_path + file_name)

def found_all_bgm(folder_path = 'assets/audio/bgm/', bgm_list = None):
    if bgm_list:
        bgm_list.clear()
        bgm_list.append('none')
        folder_path = resource_path(folder_path)
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            if '.mp3' in file_name:
                file_name = file_name.split('.')[0]
                bgm_list.append(file_name)
