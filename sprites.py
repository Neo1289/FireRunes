from libraries_and_settings import pygame, random, path, lasting_time, fire_frames


class TimeUpdate:
    def update(self, dt, name: str):
        current_time = pygame.time.get_ticks()
        self.lasting_time = lasting_time
        if (
            hasattr(self, "spawn_time")
            and (current_time - self.spawn_time) >= self.lasting_time[name]
        ):
            self.kill()


class ShootFire:
    def __init__(self, fire_frames, group):
        self.fire_frames = fire_frames
        self.all_sprites = group
        self.last_shot = 0
        self.shoot_interval = 3000

    def update(self, npc_rect):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot >= self.shoot_interval:
            fire_pos = (npc_rect.centerx + npc_rect.width // 2, npc_rect.centery)
            Fire(
                fire_pos,
                self.fire_frames,
                self.all_sprites,
                150,
                "right",
                "dragon_fire",
            )
            self.last_shot = current_time


class GeneralSprite(pygame.sprite.Sprite):
    def __init__(
        self,
        pos,
        surf,
        groups,
        ground_att: bool,
        name: str = None,
        resources: int = 0,
        item: bool = None,
    ):
        super().__init__(groups)

        self.resources = resources
        if ground_att:
            self.ground = True
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        if item:
            self.item = item
        # determine the enemy attribute
        if name:
            self.name = name
            if self.name in ("wizard", "scarecrow", "praying statue"):
                self.human = True
            if self.name == "runes":
                self.rune = True
        self.general = True


#######################
class AreaSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, groups, name=None):
        super().__init__(groups)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, width, height)
        if name in ("danger area", "river_zone"):
            self.dangerous = True
            self.damage = 1 if name == "danger area" else 1000
        if name == "trigger":
            self.trigger = True


#######################
class NPC(pygame.sprite.Sprite, TimeUpdate):
    def __init__(
        self,
        pos,
        frames,
        groups,
        name: str,
        speed: int,
        dangerous: bool,
        life: int,
        damage: int,
        direction: list = None,
        follow_player: bool = False,
        immune: str = None,
    ):
        super().__init__(groups)

        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]

        if name == "magic":
            self.animation_speed = 1
        elif name == "bush":
            self.animation_speed = 100
        else:
            self.animation_speed = 10
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.list = direction
        self.direction = pygame.Vector2(
            random.choice(self.list), random.choice(self.list)
        )
        self.speed = speed
        if dangerous:
            self.dangerous = dangerous
        self.name = name
        self.follow_player = follow_player
        self.player = None
        self.spawn_time = pygame.time.get_ticks()
        self.life = life
        self.damage = damage
        if name == "dragon" and fire_frames:
            self.shooter = ShootFire(fire_frames, groups)
        else:
            self.shooter = None
        self.immune = immune

    def animate(self, dt):
        self.frames_index += self.animation_speed * dt
        self.image = self.frames[int(self.frames_index) % len(self.frames)]

    def move(self, dt):
        if self.follow_player and self.player:
            player_pos = pygame.Vector2(self.player.rect.center)
            self.direction = (player_pos - self.pos).normalize()

        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.animate(dt)
        self.move(dt)
        if self.shooter:
            self.shooter.update(self.rect)
        TimeUpdate.update(self, dt, self.name)


class Rune(pygame.sprite.Sprite, TimeUpdate):
    def __init__(self, pos, groups, name="rune"):
        super().__init__(groups)
        self.image = pygame.image.load(
            path.join("resources", "player", "rune_bullet.png")
        ).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.spawn_time = pygame.time.get_ticks()
        self.name = name

    def update(self, dt):
        TimeUpdate.update(self, dt, Rune.__name__)


class Animation(pygame.sprite.Sprite, TimeUpdate):
    def __init__(self, pos, frames, groups, name):
        super().__init__(groups)
        self.pos = pos
        self.spawn_time = pygame.time.get_ticks()
        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect(center=pos)
        self.name = name
        if self.name == "wizard":
            self.animation_speed = 3
        elif self.name == "portal":
            self.animation_speed = 5
        else:
            self.animation_speed = 10

    def animate(self, dt):
        self.frames_index += self.animation_speed * dt
        self.image = self.frames[int(self.frames_index) % len(self.frames)]

    def update(self, dt):
        self.animate(dt)
        TimeUpdate.update(self, dt, self.name)


class Fire(pygame.sprite.Sprite, TimeUpdate):
    def __init__(self, pos, frames, groups, speed, player_state: str, name="fire"):
        super().__init__(groups)
        self.frames, self.frames_index = frames, 0
        self.image = self.frames[self.frames_index]
        self.animation_speed = 20
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.Vector2(pos)
        self.spawn_time = pygame.time.get_ticks()
        self.name = name
        self.speed = speed
        self.state = player_state

        self.direction = pygame.Vector2()
        if self.state == "up":
            self.direction = pygame.Vector2(0, -5)
        elif self.state == "down":
            self.direction = pygame.Vector2(0, 5)
        elif self.state == "left":
            self.direction = pygame.Vector2(-5, 0)
        elif self.state == "right":
            self.direction = pygame.Vector2(5, 0)

    def animate(self, dt):
        self.frames_index += self.animation_speed * dt
        self.image = self.frames[int(self.frames_index) % len(self.frames)]

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.animate(dt)
        self.move(dt)
        TimeUpdate.update(self, dt, self.name)
