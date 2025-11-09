###LIBRARIES
from libraries_and_settings import (pygame,
                                     sys,
                                     random,path)
###CONFIGURATIONS
from libraries_and_settings import (display_surface, maps, TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH,
                                     font, enemies_images, enemies_speed, enemies_direction, spawning_time, buffers, player_flame_frames, enemies_life, game_objects,
                                    enemies_damage,ice, enemies_immunity, failed_frames,water_splash_frames, fire_aura_frames,cure_frames,statue_frames, wizard_frames,portal_frames)
from words_library import phrases

###SPRITES
from player import Player
from camera import allSpritesOffset
from sprites import GeneralSprite, AreaSprite, NPC, Rune, Fire, Animation

pygame.init()
pygame.mixer.init()

class Game:
    def __init__(self):

        self.running = True
        self.display_surface = display_surface
        self.clock = pygame.time.Clock()
        ####countdowns
        self.fire_time_countdown = 0
        self.fire_buffer = 2
        self.regeneration_countdown = 0
        self.regeneration_buffer = 20
        self.last_magic_kill_time = 0

        #####key_pressed[duration time, name, effect]
        self.buffers = buffers
        self.duration_time = 0
        self.start_time = 0
        self.effect = 0
        self.buffer_used = None

        self.maps = maps  ##maps dictionary coming for the settings file
        self.current_map = None
        self.current_area = "portal"
        self.area_group = {}  ###dictionary with the areas where is possible to enter in a map
        self.transition_bool = True
        self.phrases = phrases
        self.enemies_images = enemies_images
        self.enemies_direction = enemies_direction
        self.enemies_list = list(self.enemies_images.keys())
        self.enemies_life = enemies_life
        self.enemies_damage = enemies_damage
        self.enemies_immunity = enemies_immunity
        self.obj_positions_dict = {}
        self.static_frames = {"praying statue": statue_frames, "in prayer": statue_frames, "wizard": wizard_frames, 'portal': portal_frames}

        self.collision_sprites = pygame.sprite.Group()
        self.all_sprites = allSpritesOffset()
        self.player = None
        self.player_dead = False
        self.death_start_time = 0
        self.spell_fire_augmented = False
        self.spell_ice = False
        self.spell_prayer = False

        self.spawning_time = spawning_time

        self.game_objects = game_objects
        self.weights = [0.4, 0.1, 0.49, 0.01, 0.3, 0.00001, 0.3, 0.4]
        self.last_item = ''

        self.custom_event = pygame.event.custom_type()
        self.message = ''

        self.music_loaded = False

    def load_music(self, music_file):
        """Load and play background music in loop"""

        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        self.music_loaded = True

    def cleaning_area(self):  ####removes all elements within groups

        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.area_group.clear()
        self.obj_positions_dict.clear()

    def detecting_area_name(self):  ####assigns the map based on the current area name

        if self.current_area in self.maps:
            self.current_map = self.maps[self.current_area]

    def assign_current_area(self):

        for name, area in self.area_group.items():
            if area.rect.colliderect(self.player.rect):
                if name != 'exit':
                    self.current_area = name

    def enter_area_check(self, event): ####triggering the area switch
        for name, area in self.area_group.items():
            if area.rect.colliderect(self.player.rect) and self.key_down(event, "y"):
                if name == 'forbidden forest':
                    if self.player.inventory['keys'] > 49:
                        self.player.inventory['keys'] -= 50
                        self.transition_bool = True
                    else:
                        self.message = "you need 50 keys to enter"
                elif name == 'in prayer':
                    self.areas_one()
                    continue
                else:
                    self.transition_bool = True

        ####perform the actual transition between areas
        if self.transition_bool:
            self.detecting_area_name()
            self.mapping()
            self.message = self.current_area
            self.transition_bool = False

            pygame.time.set_timer(self.custom_event, self.spawning_time[self.current_area])

    def mapping(self):

        self.cleaning_area()

        ###ground
        for x, y, image in self.current_map.get_layer_by_name('ground').tiles():
            GeneralSprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites, True)
        ###objects
        for obj in self.current_map.get_layer_by_name('objects'):
            GeneralSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites), None, obj.name, 1, item=True)
            self.obj_positions_dict[obj.name] = (obj.x, obj.y)
        ###player
        for obj in self.current_map.get_layer_by_name('areas'):
            if obj.name == 'player_spawn':
                if self.player is None:
                    self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                else:
                    self.player.collision_rect.center = (obj.x, obj.y)
                    self.all_sprites.add(self.player)

            elif obj.name not in self.enemies_list and obj.name is not None:
                self.area_group[obj.name] = AreaSprite(obj.x, obj.y, obj.width, obj.height, self.all_sprites, obj.name)
            else:
                self.monsters()

    def monsters(self):
        # Handle all enemies including fish
        for obj in self.current_map.get_layer_by_name('areas'):
            if obj.name in self.enemies_list:
                # Check if dragon already exists - only allow one dragon
                if obj.name == 'dragon':
                    existing_dragons = [sprite for sprite in self.all_sprites if
                                        isinstance(sprite, NPC) and sprite.name == 'dragon']
                    if existing_dragons:
                        continue  # Skip creating another dragon

                # Special handling for fish - pick random spawn point
                if obj.name == 'fish':
                    existing_fish = [sprite for sprite in self.all_sprites if
                                     isinstance(sprite, NPC) and sprite.name == 'fish']
                    if existing_fish:
                        continue
                    fish_areas = [o for o in self.current_map.get_layer_by_name('areas') if o.name == 'fish']
                    spawn_area = random.choice(fish_areas)
                    spawn_pos = (spawn_area.x, spawn_area.y)
                else:
                    spawn_pos = (obj.x, obj.y)

                self.monster = NPC(spawn_pos, self.enemies_images[obj.name],
                                   self.all_sprites, obj.name, enemies_speed[obj.name],
                                   True, self.enemies_life[obj.name], self.enemies_damage[obj.name], self.enemies_direction[obj.name],
                                   obj.name in ['scheleton', 'dragon', 'bat_1', 'flame_1', 'infernal_fire'], self.enemies_immunity[obj.name])

                self.monster.player = self.player

    def areas_one(self):
        for obj in self.current_map.get_layer_by_name('areas_one'):
            if obj.name in self.enemies_list:
                spawn_pos = (obj.x, obj.y)

                self.monster = NPC(spawn_pos, self.enemies_images[obj.name],
                                   self.all_sprites, obj.name, enemies_speed[obj.name],
                                   True, self.enemies_life[obj.name], self.enemies_damage[obj.name],
                                   self.enemies_direction[obj.name],
                                   follow_player=obj.name in ['scheleton', 'dragon', 'bat_1', 'flame_1',
                                                              'infernal_fire'])

                self.monster.player = self.player

    def rendering(self):
        self.text_surface = None
        ###determine the current area map to be loaded and print it
        for name, area in self.area_group.items():
            if area.rect.colliderect(self.player.rect):
                if name not in ('danger area', 'recall'):
                    self.text = f"{self.phrases['text_8']}{name}"
                    self.text_surface = font.render(self.text, True, "white")

        for obj in self.collision_sprites:
            if self.object_id(obj) and name != 'in prayer':
                self.text = f"{self.phrases['text_2']}{obj.name}?"
                self.text_surface = font.render(self.text, True, "white")
            elif self.human_id(obj):
                if obj.name == 'wizard':
                    self.text = f"{self.phrases['text_1']}"
                    self.text_surface = font.render(self.text, True, "white")
                elif obj.name == 'scarecrow':
                    self.text = f"{self.phrases['text_10']}"
                    self.text_surface = font.render(self.text, True, "white")
                elif obj.name == 'praying statue':
                    self.text = f"{self.phrases['text_13']}"
                    self.text_surface = font.render(self.text, True, "white")

        if self.text_surface:
            text_rect = self.text_surface.get_rect(center=(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 4))
            self.display_surface.blit(self.text_surface, text_rect)

    def collect_resources(self, event):
        for obj in self.collision_sprites:
            if self.object_id(obj) and obj.name != 'in prayer':
                if self.key_down(event, "y"):
                    if hasattr(obj, 'rune'):
                        self.player.inventory['runes dust'] += 1
                        obj.kill()
                        self.last_item = 'runes dust'
                    elif obj.name == 'portal':
                        obj.resources+= 1
                        if self.player.inventory['runes dust'] >= 5:
                            self.player.inventory['runes dust'] -= 5
                        else:
                            self.message = 'you need 5 runes dust'
                    else:
                        choice = random.choices(self.game_objects, weights=self.weights, k=1)[0]
                        self.player.inventory[choice] += 1
                        self.last_item = choice
                    obj.resources -= 1

    def adding_fire_dust(self):
        """Track elapsed time and automatically give player 1 fire dust every 2 seconds (max 50)."""
        self.fire_event = (pygame.time.get_ticks() - self.start_time) // 1000

        if self.preventing_repetition(self.fire_event, self.fire_time_countdown, self.fire_buffer) and self.player.inventory['fire dust'] < 50:
            self.player.inventory['fire dust'] += 1
            self.fire_time_countdown = self.fire_event

    def player_regeneration(self):
        """Track elapsed time and automatically give player 1 life dust every 10 seconds."""
        self.regeneration_event = (pygame.time.get_ticks() - self.start_time) // 1000

        if self.preventing_repetition(self.regeneration_event, self.regeneration_countdown, self.regeneration_buffer) and self.player.life < 1000 :
            self.player.life += 1
            self.regeneration_countdown = self.regeneration_event

    def player_fire(self, event):
        if self.key_down(event, 'z') and self.player.inventory['fire dust'] > 0:
            Fire(self.player.rect.center, player_flame_frames, self.all_sprites, 50, self.player.state)
            self.player.inventory['fire dust'] -= 1
        if self.key_down(event, 'x') and self.player.inventory['fire dust'] > 5 and self.spell_fire_augmented == True:
            for state in ("up", "down", "left", "right"):
                Fire(self.player.rect.center, player_flame_frames, self.all_sprites, 50, state)
            self.player.inventory['fire dust'] -= 5
        if self.key_down(event, 'c') and self.player.inventory['ice dust'] > 0 and self.spell_ice == True:
            Fire(self.player.rect.center, ice, self.all_sprites, 50, self.player.state,'ice')
            self.player.inventory['ice dust'] -= 1
        if self.key_down(event,'v') and self.player.inventory['fire dust'] > 3 and self.spell_prayer == True and self.player.life < 1000:
            self.player.inventory['fire dust'] -= 3
            self.player.life += 10
            Animation(self.player.rect.center,cure_frames,self.all_sprites,"cure_spell")

    def buffer_handlers(self, event):
        ##### buffers --> key_pressed[duration time, name, effect]
        for key, value in self.buffers.items():
            if self.key_down(event, key) and self.player.inventory[value[1]] > 0:
                self.start_time = pygame.time.get_ticks()
                self.duration_time = value[0]
                self.player.inventory[value[1]] -= 1
                self.effect = value[2]
                self.buffer_used = value[1]

    def player_buffers(self):
        self.time_event = (pygame.time.get_ticks() - self.start_time) // 1000

        if self.duration_time >= self.time_event:

            if self.buffer_used == 'runes dust':
                position = (random.choice([100, -100, 50, -50, 200, -200, 0]) + self.player.rect.x,
                            random.choice([100, -100, 50, -50, 200, -200, 0]) + self.player.rect.y)
                Rune(position, self.all_sprites)

            elif self.buffer_used == 'crystal ball':
                for enemy in self.enemies_groups():
                    if enemy.name != 'dragon':
                        enemy.speed = 0
            else:
                self.player.life += self.effect
        else:
            self.buffer_used = None

    def trading(self, event):
        for obj in self.collision_sprites:
            if self.human_id(obj):
                if obj.name == 'wizard':
                    if self.key_down(event, "s") and self.player.inventory["crystal ball"] > 0:
                        self.player.inventory["crystal ball"] -= 1
                        self.player.inventory["coin"] += 3
                    if self.key_down(event, "b") and self.player.inventory["coin"] >= 0:
                        self.player.inventory["coin"] -= 1
                        self.player.inventory["potion"] += 1
                    if self.key_down(event, "n") and self.player.inventory["coin"] >= 5:
                        self.player.inventory["coin"] -= 3
                        self.player.inventory["holy water"] += 1
                if obj.name == 'scarecrow':
                    if self.key_down(event, "s") and self.player.inventory["crystal ball"] >= 10:
                        self.player.inventory["crystal ball"] -= 10
                        self.spell_fire_augmented = True
                        self.message =  self.phrases["text_11"]
                    if self.key_down(event, "i") and self.player.inventory["crystal ball"] >= 20:
                        self.player.inventory["crystal ball"] -= 20
                        self.spell_ice= True
                        self.message = self.phrases["text_12"]
                if obj.name == 'praying statue':
                    if self.key_down(event, "p") and self.player.inventory["fire dust"] >= 50:
                        self.player.inventory["fire dust"] -= 50
                        self.spell_prayer = True
                        self.message = self.phrases["text_14"]
                        Animation(self.player.rect.center, cure_frames, self.all_sprites, "cure_spell")

    def collision_detection(self):
        for obj in self.all_sprites:
            if obj.rect.colliderect(self.player.rect):
                if hasattr(obj, "dangerous"):
                    self.player.life -= obj.damage
        if self.player.life < 0:
            self.player.life = 0

        if self.player.life > 1000:
            self.player.life = 1000

    def player_death(self):
        if self.player.life <= 0 and not self.player_dead:
            self.player_dead = True
            self.death_start_time = pygame.time.get_ticks()
            death_position = self.player.rect.center
            self.player.kill()
            if self.current_area == 'river':
                Animation(death_position, water_splash_frames, self.all_sprites, "river_zone")

        if self.player_dead:
            time_since_death = (pygame.time.get_ticks() - self.death_start_time) / 1000

            if time_since_death > 2:
                pygame.display.set_caption('GAME OVER')
                pygame.display.update()
                pygame.time.delay(3000)
                self.running = False
                pygame.quit()
                sys.exit()

    def player_aura_cast(self):
        if self.player.inventory['fire dust'] == 50:
            Animation((self.player.rect.centerx +20,self.player.rect.centery+20),fire_aura_frames,self.all_sprites, "player_aura")

    def end_game(self, event):
        for name, area in self.area_group.items():
            if area.rect.colliderect(self.player.rect) and self.key_down(event, "y") and name == 'exit':
                self.caption = pygame.display.set_caption('YOU WIN, YOU ESCAPED')
                pygame.time.delay(5000)
                pygame.quit()
                sys.exit()

    def projectiles_hit_walls(self):
        projectiles = self.player_projectiles()
        general_sprites = [sprite for sprite in self.all_sprites if
                           hasattr(sprite, 'general') and not hasattr(sprite, 'ground')]

        for general in general_sprites:
            hit_general = pygame.sprite.spritecollideany(general, projectiles)
            if hit_general:
                hit_general.kill()
                Animation(hit_general.rect.center, failed_frames, self.all_sprites, "failed_attack")

    def check_enemies_collision(self):
        enemies = self.enemies_groups()
        projectiles = self.player_projectiles()

        for enemy in enemies:
            hit_projectile = pygame.sprite.spritecollideany(enemy, projectiles)
            if hit_projectile and hit_projectile.name != enemy.immune:
                enemy.life -= 1
            if hit_projectile and hit_projectile.name == enemy.immune:
                hit_projectile.kill()
                Animation(hit_projectile.rect.center, failed_frames, self.all_sprites, 'failed_attack')

            if enemy.life <= 0:
                    enemy.kill()
                    if enemy.name == 'fish':
                        self.player.inventory['keys'] += 1
                        self.last_item = 'key'
                    if enemy.name == 'dragon':
                        self.player.inventory['coin'] += 20
                        self.player.inventory['keys'] += 2
                        self.player.inventory['crystal ball'] += 2
                    if enemy.name == 'magic':
                        current_time = pygame.time.get_ticks() // 1000
                        if self.preventing_repetition(current_time, self.last_magic_kill_time, 1) and self.regeneration_buffer > 5:
                            self.regeneration_buffer -= 1
                            self.last_magic_kill_time = current_time
                            self.message = f"your regeneration rank is now {self.regeneration_buffer}"
                        self.areas_one()

    def display_captions(self):
        time_sec = pygame.time.get_ticks() // 1000
        enemies = self.enemies_groups()

        self.caption = (f"\u2665 {self.player.life}     "
                        f"\U0001F9EA {self.player.inventory['potion']}     "
                        f"\U0001F52E {self.player.inventory['crystal ball']}     "
                        f"\U0001F4B0 {self.player.inventory['coin']}     "
                        f"\U0001F5DD {self.player.inventory['keys']}     "
                        f"\u2697\ufe0f {self.player.inventory['holy water']}     "
                        f"\U0001F4AB {self.player.inventory['runes dust']}     "
                        f"\U0001F525 {self.player.inventory['fire dust']}     "
                        f"\u2744\uFE0F {self.player.inventory['ice dust']}     "
                        f"timer: {time_sec}          "
                        f"last item found: {self.last_item}      "
                        f"special enemy life: {[i.life for i in enemies if i.name == 'dragon']}      "
                        f"{self.message}"
                        )
        pygame.display.set_caption(self.caption)

    ################################
    ####REDUNDANT CODE REDUCTION####
    ################################
    def object_id(self, obj):
        if obj.rect.colliderect(self.player.rect) and hasattr(obj, "name") and hasattr(obj, "item") and not hasattr(obj, "human") and obj.resources > 0:
            return True

    def human_id(self, obj):
        if obj.rect.colliderect(self.player.rect) and hasattr(obj, "human"):
            return True

    def key_down(self, event, key: str):
        if event.type == pygame.KEYDOWN:
            self.key_event = pygame.key.name(event.key)
        return event.type == pygame.KEYDOWN and event.key == getattr(pygame, f"K_{key}")

    def enemies_groups(self):
        return [sprite for sprite in self.all_sprites if isinstance(sprite, NPC)]

    def preventing_repetition(self,time_event,any_time_attribute, buffer: int):
        """Prevent duplicate actions
        by checking if current time is even and different from last action time."""
        return time_event % buffer == 0 and time_event != any_time_attribute

    def player_projectiles(self):
        projectiles = pygame.sprite.Group([
            sprite for sprite in self.all_sprites
            if isinstance(sprite, (Rune, Fire))
        ])
        return projectiles

    def main_menu(self):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu_running = False
                    elif event.key == pygame.K_q:
                        self.running = False
                        return

            self.display_surface.fill('black')

            # Create text surfaces
            title = font.render("GAME MENU", True, "white")

            # Position title at top
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 6))

            self.display_surface.blit(title, title_rect)

            pygame.display.update()

    def static_animations(self):
        """ this method is intended for static animation for objects
        not for players or other dynamic triggers like projectiles"""
        keys = ['praying statue', 'in prayer','wizard', 'portal']

        for key in keys:
            if key in self.obj_positions_dict:
                Animation(self.obj_positions_dict[key], self.static_frames[key], self.all_sprites, key)

    def run(self):

        while self.running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                self.enter_area_check(event)
                self.collect_resources(event)
                self.trading(event)
                self.buffer_handlers(event)
                self.player_fire(event)
                self.end_game(event)
                if event.type == self.custom_event:
                    self.monsters()
                    self.static_animations()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.main_menu()
                    continue

            self.adding_fire_dust()
            self.player_regeneration()
            self.player_aura_cast()
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.rect.center)
            self.rendering()
            self.display_captions()
            self.collision_detection()
            self.player_death()
            self.check_enemies_collision()
            self.projectiles_hit_walls()
            self.player_buffers()
            self.assign_current_area()

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    main_game = Game()
    main_game.run()
