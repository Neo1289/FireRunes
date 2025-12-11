# ---------------------------
# importing libraries
# ---------------------------
import pygame
import sys
import os
from os import path, walk, listdir
from os.path import join
import pymunk
from pytmx.util_pygame import load_pygame
import random

pygame.init()

# ---------------------------
# Get the correct base path for resources
# ---------------------------
if getattr(sys, "frozen", False):
    # Running as PyInstaller executable
    BASE_PATH = sys._MEIPASS
else:
    # Running as normal Python script
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def get_resource_path(*args):
    """Get the correct path to resources, whether running as script or executable."""
    return os.path.join(BASE_PATH, "resources", *args)


# ---------------------------
# Configuration Parameters
# ---------------------------
screen_size = pygame.display.get_desktop_sizes()[0]
WINDOW_WIDTH = int(screen_size[0] * 0.9)
WINDOW_HEIGHT = int(screen_size[1] * 0.85)
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
TILE_SIZE = 32
font = pygame.font.Font(None, 22)

# ---------------------------
# maps
# ---------------------------
maps = {}
for dirpath, dirnames, filenames in walk(get_resource_path("world")):
    for filename in filenames:
        if filename.lower().endswith(".tmx"):
            maps[(filename.split(".")[0])] = load_pygame(
                get_resource_path("world", filename)
            )

# ------------------------------------------
# images
# ------------------------------------------

images_dictionary = {
    "bat": [],
    "special_bat": [],
    "bush": [],
    "skeleton": [],
    "special_skeleton": [],
    "ice_attack": [],
    "fish": [],
    "torch": [],
}

color_key = {
    "bat": None,
    "special_bat": None,
    "bush": None,
    "skeleton": None,
    "special_skeleton": None,
    "ice_attack": None,
    "fish": None,
    "torch": (10, 5, 46),
    "power_of_king": "black",
}

for enemy_name in images_dictionary:
    folder = get_resource_path(enemy_name)
    for file_name in listdir(folder):
        full_path = path.join(folder, file_name)
        if color_key[enemy_name] is None:
            surf = pygame.image.load(full_path).convert_alpha()
        elif color_key[enemy_name] is not None:
            surf = pygame.image.load(full_path).convert()
            surf.set_colorkey((10, 5, 46))
        images_dictionary[enemy_name].append(surf)


# ---------------------------
# dragon images
# ---------------------------

dragon = []
dragon_folder = get_resource_path("dragon", "left")
for file_name in listdir(dragon_folder):
    full_path = path.join(dragon_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    dragon.append(surf)


# ---------------------------
# infernal fire images
# ---------------------------

infernal = []
infernal_folder = get_resource_path("fire_attack")
for file_name in listdir(infernal_folder):
    full_path = path.join(infernal_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    surf.set_colorkey((31, 16, 42))
    infernal.append(surf)

# ---------------------------
# magic stone images
# ---------------------------

magic = []

magic_folder = get_resource_path("magic_stone")
for file_name in listdir(magic_folder):
    full_path = path.join(magic_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    surf.set_colorkey((31, 16, 42))
    magic.append(surf)

# ---------------------------
# player flame images
# ---------------------------

player_flame_frames = []
player_flame_folder = get_resource_path("player_flame")
for file_name in listdir(player_flame_folder):
    full_path = path.join(player_flame_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((31, 16, 42))
    player_flame_frames.append(surf)

# ---------------------------
# dragon flame images
# ---------------------------

fire_frames = []
fire_flame_folder = get_resource_path("dragon_flame")
for file_name in listdir(fire_flame_folder):
    full_path = path.join(fire_flame_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((31, 16, 42))
    fire_frames.append(surf)

# ---------------------------
# water splash images
# ---------------------------

water_splash_frames = []
water_splash_folder = get_resource_path("water_splash")
for file_name in listdir(water_splash_folder):
    full_path = path.join(water_splash_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    water_splash_frames.append(surf)

# ---------------------------
# player dragon aurea images
# ---------------------------

player_dragon_frames = []
player_dragon_folder = get_resource_path("player_dragon_aura")
for file_name in listdir(player_dragon_folder):
    full_path = path.join(player_dragon_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    player_dragon_frames.append(surf)

# ---------------------------
# failed attack images
# ---------------------------

failed_frames = []
failed_folder = get_resource_path("failed_attack")
for file_name in listdir(failed_folder):
    full_path = path.join(failed_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    failed_frames.append(surf)
# ---------------------------

# grass images
# ---------------------------

grass_frames = []
grass_folder = get_resource_path("grass")
for file_name in listdir(grass_folder):
    full_path = path.join(grass_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    grass_frames.append(surf)

# ---------------------------
# player fire aura
# ---------------------------

fire_aura_frames = []
aura_folder = get_resource_path("player_aura")
for file_name in listdir(aura_folder):
    full_path = path.join(aura_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((31, 16, 42))
    fire_aura_frames.append(surf)
# ---------------------------
# player fire aura
# ---------------------------

cure_frames = []
cure_folder = get_resource_path("cure_spell")
for file_name in listdir(cure_folder):
    full_path = path.join(cure_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((0, 128, 128))
    cure_frames.append(surf)

# ---------------------------
# praying statue aura
# ---------------------------

statue_frames = []
statue_folder = get_resource_path("statue_energy")
for file_name in listdir(statue_folder):
    full_path = path.join(statue_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((0, 128, 128))
    statue_frames.append(surf)

# ---------------------------
# wizard
# ---------------------------

wizard_frames = []
wizard_folder = get_resource_path("wizard")
for file_name in listdir(wizard_folder):
    full_path = path.join(wizard_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    wizard_frames.append(surf)

# ---------------------------
# wizard
# ---------------------------

necro_frames = []
necro_folder = get_resource_path("necromancer")
for file_name in listdir(necro_folder):
    full_path = path.join(necro_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    necro_frames.append(surf)

# ---------------------------
# portal
# ---------------------------

portal_frames = []
portal_folder = get_resource_path("portal")
for file_name in listdir(portal_folder):
    full_path = path.join(portal_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    portal_frames.append(surf)


# ---------------------------
# inventory map
# ---------------------------
inventory_map = pygame.image.load(get_resource_path("map.png")).convert()

# ------------------------------------
# dictionaries and lists of useful stuff
# -------------------------------------

enemies_damage = {
    "dragon": 4,
    "bat": 0.5,
    "bat_1": 1,
    "special_bat": 3,
    "scheleton": 0.5,
    "fish": 0.1,
    "flame": 3,
    "flame_1": 3,
    "ice": 3,
    "infernal_fire": 5,
    "magic": 0.5,
    "bush": 1,
    "special_scheleton": 3,
}
enemies_life = {
    "dragon": 500,
    "bat": 1,
    "bat_1": 1,
    "special_bat": 70,
    "scheleton": 1,
    "fish": 1,
    "flame": 100000,
    "flame_1": 10,
    "ice": 1000,
    "infernal_fire": 10000,
    "magic": 3,
    "bush": 1,
    "special_scheleton": 100,
}
enemies_images = {
    "dragon": dragon,
    "bat": images_dictionary["bat"],
    "bat_1": images_dictionary["bat"],
    "special_bat": images_dictionary["special_bat"],
    "scheleton": images_dictionary["skeleton"],
    "fish": images_dictionary["fish"],
    "flame": images_dictionary["torch"],
    "flame_1": images_dictionary["torch"],
    "ice": images_dictionary["ice_attack"],
    "infernal_fire": infernal,
    "magic": magic,
    "bush": images_dictionary["bush"],
    "special_scheleton": images_dictionary["special_skeleton"],
}

enemies_speed = {
    "dragon": 110,
    "bat": 80,
    "bat_1": 80,
    "special_bat": 100,
    "scheleton": 30,
    "fish": 5,
    "flame": 0,
    "flame_1": 7,
    "ice": 100,
    "infernal_fire": 100,
    "magic": 0,
    "bush": 0,
    "special_scheleton": 30,
}
enemies_direction = {
    "dragon": [-1, 1],
    "bat": [-1, 1],
    "bat_1": [-1, 1],
    "special_bat": [-1, 1],
    "scheleton": [-1, 1],
    "fish": [-1, 1],
    "flame": [-1, 1],
    "flame_1": [-1, 1],
    "ice": [-1, 1],
    "infernal_fire": [-1, 1],
    "magic": [-1, 1],
    "bush": [-1, 1],
    "special_scheleton": [-1, 1],
}
enemies_immunity = {
    "dragon": "fire",
    "bat": None,
    "bat_1": None,
    "special_bat": None,
    "scheleton": "ice",
    "fish": None,
    "flame": "fire",
    "flame_1": "fire",
    "ice": "ice",
    "infernal_fire": "fire",
    "magic": None,
    "bush": None,
    "special_scheleton": "ice",
}
spawning_time = {
    "world": 20000,
    "house": 2000,
    "forest": 700,
    "cemetery": 500,
    "dungeon": 100000000,
    "maze": 2500,
    "abandoned house": 500,
    "river": 2000,
    "forbidden forest": 50,
    "exit": 0,
    "hidden door": 1000,
    "portal": 1000,
    "tavern": 1000000,
    "citizen house": 100000000,
    "scarecrow house": 0,
}

lasting_time = {
    "Rune": 1000,
    "scheleton": 30000,
    "flame": 300000000,
    "dragon": 3000000,
    "ice": 1000,
    "bat_1": 50000,
    "bat": 10000,
    "special_bat": 100000,
    "fire": 1000,
    "fish": 2000,
    "flame_1": 100000,
    "infernal_fire": 2000,
    "magic": 5000,
    "bush": 2000,
    "failed_attack": 100,
    "power_of_king": 600,
    "grass": 1000,
    "dragon_fire": 1000,
    "river_zone": 50,
    "player_aura": 100,
    "cure_spell": 500,
    "praying statue": 700,
    "in prayer": 600,
    "wizard": 10000,
    "necromancer": 20000,
    "portal": 20000,
    "special_scheleton": 30000000,
    "player_dragon_aura": 100,
}

game_objects = [
    "potion",
    "crystal ball",
    "coin",
    "runes dust",
    "nothing useful",
    "holy water",
    "fire dust",
    "ice dust",
]

buffers = {
    "1": [0, "potion", 2],
    "3": [10, "holy water", 1],
    "2": [0, "crystal ball", 0],
    "4": [1, "runes dust", 0],
}
