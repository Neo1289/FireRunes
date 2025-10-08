###LIBRARIES
from libraries_and_settings import (pygame,
                                    sys,
                                    random)
###CONFIGURATIONS
from libraries_and_settings import (display_surface, maps, TILE_SIZE, WINDOW_HEIGHT,WINDOW_WIDTH,
                                    font,enemies_images,enemies_speed,enemies_direction,spawning_time,key_dict,player_flame_frames,enemies_life)
from words_library import phrases,instructions,trade,items

###SPRITES
from player import Player
from camera import allSpritesOffset
from sprites import GeneralSprite,AreaSprite,NPC,Rune,Fire

pygame.init()

class Game:
    def __init__(self):

        self.running = True
        self.display_surface = display_surface
        self.clock = pygame.time.Clock()
        self.start_time = 0
        self.duration_time = 0
        self.temporary_action = None
        self.key_dict = key_dict
        self.last_time_guard = 0

        self.maps = maps
        self.current_map = None
        self.current_area = "world"
        self.area_group = {}
        self.transition_bool = True
        self.phrases = phrases
        self.enemies_images = enemies_images
        self.enemies_direction = enemies_direction
        self.enemies_list = list(self.enemies_images.keys())
        self.enemies_life = enemies_life
        self.instructions = instructions
        self.trade = trade
        self.items = items

        self.collision_sprites = pygame.sprite.Group()
        self.all_sprites = allSpritesOffset()
        self.player = None

        self.spawning_time = spawning_time

        self.game_objects = ['potion','crystal ball','coin','runes dust','nothing useful','holy water','fire dust']
        self.weights = [0.4,0.1,0.49,0.01,1,0.00001,0.3]
        self.last_item = ''

        self.custom_event = pygame.event.custom_type()

    def mapping(self):

        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.area_group.clear()

        for name, map in self.maps.items():
            if name == self.current_area:
                self.current_map = map
        ###ground
        for x, y, image in self.current_map.get_layer_by_name('ground').tiles():
            GeneralSprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites,True)
        ###objects
        for obj in self.current_map.get_layer_by_name('objects'):
            GeneralSprite((obj.x, obj.y), obj.image, (self.all_sprites,self.collision_sprites),None,obj.name,1,item= True)
        ###player
        for obj in self.current_map.get_layer_by_name('areas'):
            if obj.name == 'player_spawn':
                if self.player is None:
                    self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                else:
                    self.player.collision_rect.center = (obj.x, obj.y)
                    self.all_sprites.add(self.player)

            elif obj.name not in self.enemies_list and obj.name is not None:
                self.area_group[obj.name] = AreaSprite(obj.x, obj.y, obj.width, obj.height, self.all_sprites,obj.name)
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
                    fish_areas = [o for o in self.current_map.get_layer_by_name('areas') if o.name == 'fish']
                    spawn_area = random.choice(fish_areas)
                    spawn_pos = (spawn_area.x, spawn_area.y)
                else:
                    spawn_pos = (obj.x, obj.y)

                self.monster = NPC(spawn_pos, self.enemies_images[obj.name],
                                   self.all_sprites, obj.name, enemies_speed[obj.name],
                                   True, self.enemies_life[obj.name], self.enemies_direction[obj.name],
                                   follow_player=obj.name in ['scheleton', 'dragon', 'bat_1', 'flame_1'])
                self.monster.player = self.player
                
    def enter_area_check(self,event):
        for name, area in self.area_group.items():
        ###check if the player pressed yes key to enter the area
            if area.rect.colliderect(self.player.rect) and self.key_down(event,"y"):
                if name not in ('forbidden forest','exit'):
                    self.transition_bool = True
                elif name == 'forbidden forest' and self.player.inventory['keys'] > 4:
                    self.player.inventory['keys'] -= 5
                    self.transition_bool = True

        ###perform the actual transition between areas
        if self.transition_bool:
            self.mapping()
            self.transition_bool = False

            pygame.time.set_timer(self.custom_event, self.spawning_time[self.current_area])

    def rendering(self):
        self.text_surface = None
        ###determine the current area map to be loaded and print it
        for name, area in self.area_group.items():
            if area.rect.colliderect(self.player.rect):
                    if name not in ('danger area','recall'):
                        self.current_area = name
                        self.text = f"{self.phrases['text_8']}{name}"
                        self.text_surface = font.render(self.text,True,"white")

        for obj in self.collision_sprites:
            if self.object_id(obj):
               self.text = f"{self.phrases["text_2"]}{obj.name}?"
               self.text_surface = font.render(self.text, True, "white")
            elif self.human_id(obj):
                self.text = f"{self.phrases["text_1"]}"
                self.text_surface = font.render(self.text, True, "white")

        if self.text_surface:
            text_rect = self.text_surface.get_rect(center=(WINDOW_WIDTH // 3, WINDOW_HEIGHT // 4))
            self.display_surface.blit(self.text_surface, text_rect)

    def collect_resources(self,event):
        for obj in self.collision_sprites:
            if self.object_id(obj):
                if self.key_down(event, "y"):
                    if hasattr(obj,'rune'):
                        self.player.inventory['runes dust']+= 1
                        obj.kill()
                        self.last_item = 'runes dust'
                    else:
                        choice = random.choices(self.game_objects,weights=self.weights,k=1)[0]
                        self.player.inventory[choice]+= 1
                        self.last_item = choice
                    obj.resources -= 1

    def event_timer(self):
        self.time_event = (pygame.time.get_ticks() - self.start_time) // 1000

        if self.preventing_repetition() and self.player.inventory['fire dust'] < 50:
            self.player.inventory['fire dust'] += 1
            self.last_time_guard = self.time_event

    def reset_timer(self, event):
        for key,value in self.key_dict.items():
            #####value[time,action name,effect]
            if self.key_down(event, key) and self.player.inventory[value[1]] > 0:
                self.start_time = pygame.time.get_ticks()
                self.duration_time = value[0]
                self.player.inventory[value[1]] -= 1
                self.temporary_action = value[1]
                self.effect = value[2]

    def player_buffers(self):
        enemies = self.enemies_groups()
        for obj in self.game_objects:
            if self.duration_time >= self.time_event and self.temporary_action == obj:
                self.player.life += self.effect
                if self.temporary_action == 'runes dust':
                    position = (random.choice([100, -100, 50, -50, 200, -200, 0]) + self.player.rect.x,
                                        random.choice([100, -100, 50, -50, 200, -200, 0]) + self.player.rect.y)
                    Rune(position, self.all_sprites)
                if self.temporary_action == 'crystal ball':
                    for enemy in enemies:
                        if enemy.name != 'dragon':
                            enemy.speed = 0

    def player_fire(self,event):
        if self.key_down(event,'z') and self.player.inventory['fire dust'] > 0:
            Fire(self.player.rect.center,player_flame_frames,self.all_sprites,50,self.player.state)
            self.player.inventory['fire dust'] -= 1

    def trading(self,event):
        for obj in self.collision_sprites:
            if self.human_id(obj):
                if self.key_down(event,"s") and self.player.inventory["crystal ball"] > 0:
                    self.player.inventory["crystal ball"] -= 1
                    self.player.inventory["coin"] += 3
                if self.key_down(event, "b") and self.inventory["coin"] >= 0:
                    self.player.inventory["coin"] -= 1
                    self.player.inventory["potion"] += 1
                if self.key_down(event, "n") and self.inventory["coin"] >= 5:
                    self.player.inventory["coin"] -= 3
                    self.player.inventory["holy water"] += 1

    def collision_detection(self):
        for obj in self.all_sprites:
            if obj.rect.colliderect(self.player.rect):
                if hasattr(obj, "dangerous"): self.player.life -= 1

        if self.player.life <= 0:
            self.caption = pygame.display.set_caption('GAME OVER')
            pygame.time.delay(5000)
            pygame.quit()
            sys.exit()

    def end_game(self,event):
        for name, area in self.area_group.items():
            if area.rect.colliderect(self.player.rect) and self.key_down(event, "y") and name == 'exit':
                self.caption = pygame.display.set_caption('YOU WIN, YOU ESCAPED')
                pygame.time.delay(5000)
                pygame.quit()
                sys.exit()

    def check_enemies_collision(self):
        enemies = self.enemies_groups()
        projectiles = pygame.sprite.Group([
            sprite for sprite in self.all_sprites
            if isinstance(sprite, (Rune, Fire))
        ])
        self.fishes = 0
        for enemy in enemies:
            if pygame.sprite.spritecollideany(enemy, projectiles):
                enemy.life -= 1
            if enemy.life == 0:
                enemy.kill()
                if enemy.name =='fish':
                    self.player.inventory['keys'] += 1
                if enemy.name == 'dragon':
                    self.player.inventory['coin'] += 20
                    self.player.inventory['keys'] += 2
                    self.player.inventory['crystal ball'] += 2

        for sprite in self.all_sprites: #controlling fishes population
            if isinstance(sprite, NPC) and sprite.name == 'fish':
                self.fishes += 1
            if self.fishes > 1:
                self.all_sprites.remove(sprite)

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
                        f"\U0001F525{self.player.inventory['fire dust']}     "
                        f"timer: {time_sec}          "
                        f"last item found: {self.last_item}     "
                        f"special enemy life: {[i.life for i in enemies if i.name in ('dragon','fish')]}"
                        )
        pygame.display.set_caption(self.caption)

    ################################
    ####REDUNDANT CODE REDUCTION####
    ################################
    def object_id(self,obj):
        if obj.rect.colliderect(self.player.rect) and hasattr(obj, "name") and hasattr(obj,
                                                                                           "item") and not hasattr(obj,
                                                                                           "human")  and obj.resources > 0:
            return True

    def human_id(self,obj):
        if obj.rect.colliderect(self.player.rect) and hasattr(obj, "human"):
            return True

    def key_down(self, event, key: str):
        if event.type == pygame.KEYDOWN:
            self.key_event = pygame.key.name(event.key)
        return event.type == pygame.KEYDOWN and event.key == getattr(pygame, f"K_{key}")

    def enemies_groups(self):
        return [sprite for sprite in self.all_sprites if isinstance(sprite, NPC)]

    def preventing_repetition(self):
        return  self.time_event % 2 == 0 and self.time_event != self.last_time_guard

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

            # Menu text
            title = font.render("GAME MENU", True, "white")
            instructions_text = font.render(f"{self.instructions}", True, "white")
            trade_text = font.render(f"{self.trade}", True, "white")
            items_text = font.render(f"{self.items}", True, "white")
            controls = font.render("ESC - Resume | Q - Quit", True, "white")

            # Center the text
            title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
            instructions_rect = instructions_text.get_rect(center=(WINDOW_WIDTH // 2, 200))
            trade_rect = trade_text.get_rect(center=(WINDOW_WIDTH // 2, 300))
            items_rect = items_text.get_rect(center=(WINDOW_WIDTH // 2, 400))
            controls_rect = controls.get_rect(center=(WINDOW_WIDTH // 2, 500))

            menu_dict = {
                title: title_rect,
                instructions_text: instructions_rect,
                trade_text: trade_rect,
                items_text: items_rect,
                controls: controls_rect
            }

            for key,value in menu_dict.items():
                self.display_surface.blit(key, value)

            pygame.display.update()

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
                self.reset_timer(event)
                self.player_fire(event)
                self.end_game(event)
                if event.type == self.custom_event:
                    self.monsters()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    self.main_menu()
                    continue

            self.event_timer()
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.player.rect.center)
            self.rendering()
            self.display_captions()
            self.collision_detection()
            self.check_enemies_collision()
            self.player_buffers()

            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    main_game = Game()
    main_game.run()
    main_game.mapping()