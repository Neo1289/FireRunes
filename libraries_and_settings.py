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
    "fire_attack": [],
    "magic_stone": [],
    "player_flame": [],
    "dragon_flame": [],
    "water_splash": [],
    "player_dragon_aura": [],
    "failed_attack": [],
    "grass": [],
    "player_aura": [],
    "cure_spell": [],
    "statue_energy": [],
    "wizard": [],
    "necromancer": [],
    "portal": [],
    "dragon": [],
    "cauldron": []
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
    "fire_attack": (31, 16, 42),
    "magic_stone": "black",
    "player_flame": (31, 16, 42),
    "dragon_flame": (31, 16, 42),
    "water_splash": "black",
    "player_dragon_aura": "black",
    "failed_attack": "black",
    "grass": "black",
    "player_aura": (31, 16, 42),
    "cure_spell": (0, 128, 128),
    "statue_energy": (0, 128, 128),
    "wizard": "black",
    "necromancer": "black",
    "portal": "black",
    "dragon": None,
    "cauldron": (106, 90, 116)
}

for enemy_name in images_dictionary:
    folder = get_resource_path(enemy_name)
    for file_name in listdir(folder):
        full_path = path.join(folder, file_name)
        if color_key[enemy_name] is None:
            surf = pygame.image.load(full_path).convert_alpha()
        elif color_key[enemy_name] is not None:
            surf = pygame.image.load(full_path).convert()
            surf.set_colorkey(color_key[enemy_name])
        images_dictionary[enemy_name].append(surf)

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
    "dragon": images_dictionary["dragon"],
    "bat": images_dictionary["bat"],
    "bat_1": images_dictionary["bat"],
    "special_bat": images_dictionary["special_bat"],
    "scheleton": images_dictionary["skeleton"],
    "fish": images_dictionary["fish"],
    "flame": images_dictionary["torch"],
    "flame_1": images_dictionary["torch"],
    "ice": images_dictionary["ice_attack"],
    "infernal_fire": images_dictionary["fire_attack"],
    "magic": images_dictionary["magic_stone"],
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
    "cauldron": 500
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
