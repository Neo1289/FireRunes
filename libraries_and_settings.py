# ---------------------------
# importing libraries
# ---------------------------
import pygame
import sys
from os import path, walk, listdir
from os.path import join
import pymunk
from pytmx.util_pygame import load_pygame
import random

pygame.init()

# ---------------------------
# Configuration Parameters
# ---------------------------
WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 768
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
TILE_SIZE = 32
font = pygame.font.Font(None, 22)

# ---------------------------
# maps
# ---------------------------
maps = {}
for dirpath, dirnames, filenames in walk(path.join("resources", "world")):
    for filename in filenames:
        if filename.lower().endswith(".tmx"):
            maps[(filename.split(".")[0])] = load_pygame(
                path.join("resources", "world", filename)
            )

# ---------------------------
# bats images
# ---------------------------

bat = []
bat_folder = path.join("resources", "bat")
for file_name in listdir(bat_folder):
    full_path = path.join(bat_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    bat.append(surf)

# ---------------------------
# special bats images
# ---------------------------

special_bat = []
special_bat_folder = path.join("resources", "special_bat")
for file_name in listdir(special_bat_folder):
    full_path = path.join(special_bat_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    special_bat.append(surf)

# ---------------------------
# bush images
# ---------------------------

bush = []
bush_folder = path.join("resources", "bush")
for file_name in listdir(bush_folder):
    full_path = path.join(bush_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    bush.append(surf)

# ---------------------------
# scheletons images
# ---------------------------

scheleton = []
scheleton_folder = path.join("resources", "skeleton")
for file_name in listdir(scheleton_folder):
    full_path = path.join(scheleton_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    scheleton.append(surf)

# ---------------------------
# scheletons images
# ---------------------------

special_scheleton = []
special_scheleton_folder = path.join("resources", "special_skeleton")
for file_name in listdir(special_scheleton_folder):
    full_path = path.join(special_scheleton_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    special_scheleton.append(surf)


# ---------------------------
# flames images
# ---------------------------

flame = []
flame_folder = path.join("resources", "torch")
for file_name in listdir(flame_folder):
    full_path = path.join(flame_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((10, 5, 46))
    flame.append(surf)

# ---------------------------
# ice images
# ---------------------------

ice = []
ice_folder = path.join("resources", "ice_attack")
for file_name in listdir(ice_folder):
    full_path = path.join(ice_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    ice.append(surf)

# ---------------------------
# dragon images
# ---------------------------

dragon = []
dragon_folder = path.join("resources", "dragon", "left")
for file_name in listdir(dragon_folder):
    full_path = path.join(dragon_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    dragon.append(surf)

# ---------------------------
# fish images
# ---------------------------

fish = []
fish_folder = path.join("resources", "fish")
for file_name in listdir(fish_folder):
    full_path = path.join(fish_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    fish.append(surf)

# ---------------------------
# infernal fire images
# ---------------------------

infernal = []
infernal_folder = path.join("resources", "fire_attack")
for file_name in listdir(infernal_folder):
    full_path = path.join(infernal_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    surf.set_colorkey((31, 16, 42))
    infernal.append(surf)

# ---------------------------
# magic stone images
# ---------------------------

magic = []

magic_folder = path.join("resources", "magic_stone")
for file_name in listdir(magic_folder):
    full_path = path.join(magic_folder, file_name)
    surf = pygame.image.load(full_path).convert_alpha()
    surf.set_colorkey((31, 16, 42))
    magic.append(surf)

# ---------------------------
# player flame images
# ---------------------------

player_flame_frames = []
player_flame_folder = path.join("resources", "player_flame")
for file_name in listdir(player_flame_folder):
    full_path = path.join(player_flame_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((31, 16, 42))
    player_flame_frames.append(surf)

# ---------------------------
# dragon flame images
# ---------------------------

fire_frames = []
fire_flame_folder = path.join("resources", "dragon_flame")
for file_name in listdir(fire_flame_folder):
    full_path = path.join(fire_flame_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((31, 16, 42))
    fire_frames.append(surf)

# ---------------------------
# water splash images
# ---------------------------

water_splash_frames = []
water_splash_folder = path.join("resources", "water_splash")
for file_name in listdir(water_splash_folder):
    full_path = path.join(water_splash_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    water_splash_frames.append(surf)

# ---------------------------
# failed attack images
# ---------------------------

failed_frames = []
failed_folder = path.join("resources", "failed_attack")
for file_name in listdir(failed_folder):
    full_path = path.join(failed_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    failed_frames.append(surf)

# ---------------------------
# player fire aura
# ---------------------------

fire_aura_frames = []
aura_folder = path.join("resources", "player_aura")
for file_name in listdir(aura_folder):
    full_path = path.join(aura_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((31, 16, 42))
    fire_aura_frames.append(surf)
# ---------------------------
# player fire aura
# ---------------------------

cure_frames = []
cure_folder = path.join("resources", "cure_spell")
for file_name in listdir(cure_folder):
    full_path = path.join(cure_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((0, 128, 128))
    cure_frames.append(surf)

# ---------------------------
# praying statue aura
# ---------------------------

statue_frames = []
statue_folder = path.join("resources", "statue_energy")
for file_name in listdir(statue_folder):
    full_path = path.join(statue_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey((0, 128, 128))
    statue_frames.append(surf)

# ---------------------------
# wizard
# ---------------------------

wizard_frames = []
wizard_folder = path.join("resources", "wizard")
for file_name in listdir(wizard_folder):
    full_path = path.join(wizard_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    wizard_frames.append(surf)

# ---------------------------
# wizard
# ---------------------------

necro_frames = []
necro_folder = path.join("resources", "necromancer")
for file_name in listdir(necro_folder):
    full_path = path.join(necro_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    necro_frames.append(surf)

# ---------------------------
# portal
# ---------------------------

portal_frames = []
portal_folder = path.join("resources", "portal")
for file_name in listdir(portal_folder):
    full_path = path.join(portal_folder, file_name)
    surf = pygame.image.load(full_path).convert()
    surf.set_colorkey("black")
    portal_frames.append(surf)


# ---------------------------
# inventory map
# ---------------------------
inventory_map = pygame.image.load(path.join("resources", "map.png")).convert()

# ------------------------------------
# dictionaries and lists of useful stuff
# -------------------------------------

enemies_damage = {
    "dragon": 4,
    "bat": 0.5,
    "bat_1": 1,
    "special_bat": 5,
    "scheleton": 0.5,
    "fish": 0.1,
    "flame": 3,
    "flame_1": 3,
    "ice": 3,
    "infernal_fire": 20,
    "magic": 10,
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
    "magic": 30,
    "bush": 1,
    "special_scheleton": 100,
}
enemies_images = {
    "dragon": dragon,
    "bat": bat,
    "bat_1": bat,
    "special_bat": special_bat,
    "scheleton": scheleton,
    "fish": fish,
    "flame": flame,
    "flame_1": flame,
    "ice": ice,
    "infernal_fire": infernal,
    "magic": magic,
    "bush": bush,
    "special_scheleton": special_scheleton,
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
    "magic": "fire",
    "bush": None,
    "special_scheleton": "ice",
}
spawning_time = {
    "world": 5000,
    "house": 2000,
    "forest": 7000,
    "cemetery": 5000,
    "dungeon": 100000000,
    "maze": 2500,
    "abandoned house": 5000,
    "river": 2000,
    "forbidden forest": 5000,
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
    "dragon_fire": 1000,
    "river_zone": 50,
    "player_aura": 100,
    "cure_spell": 500,
    "praying statue": 700,
    "in prayer": 600,
    "wizard": 10000,
    "necromancer": 5000,
    "portal": 10000,
    "special_scheleton": 30000000,
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
