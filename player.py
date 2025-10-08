from libraries_and_settings import pygame, walk, path, join

class Player(pygame.sprite.Sprite):
    # Class constants
    SPEED = 200
    COLLISION_SHRINK = 30
    ANIMATION_SPEED = 10
    INITIAL_LIFE = 1000

    # Direction mappings for cleaner code
    DIRECTIONS = {
        'horizontal': ('x', 'centerx', 'left', 'right'),
        'vertical': ('y', 'centery', 'top', 'bottom')
    }

    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)

        # Initialize state
        self.state = 'down'
        self.frame_index = 0
        self.direction = pygame.Vector2()
        self.life = self.INITIAL_LIFE

        # Store references
        self.collision_sprites = collision_sprites
        self.groups = groups

        # Load and setup graphics
        self._load_images()
        self._setup_rects(pos)

        self.inventory = {
            'potion': 1,
            'crystal ball': 1,
            'coin': 1,
            'keys': 5,
            'holy water': 1,
            'runes dust': 1,
            'nothing useful': 0,
            'fire dust': 1
        }

    def _setup_rects(self, pos):
        """Initialize player rectangles for rendering and collision"""
        self.image = self.frames[self.state][0]
        self.rect = self.image.get_rect(center=pos)
        self.collision_rect = self.rect.inflate(-self.COLLISION_SHRINK, -self.COLLISION_SHRINK)

    def _load_images(self):
        """Load all animation frames for each direction"""
        self.frames = {direction: [] for direction in ['left', 'right', 'up', 'down']}

        for state in self.frames.keys():
            folder_path = path.join('resources', 'player', state)
            for folder, _, file_names in walk(folder_path):
                if file_names:
                    # Sort files numerically and load them
                    sorted_files = sorted(file_names, key=lambda name: int(name.split('.')[0]))
                    for file_name in sorted_files:
                        full_path = join(folder, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def _get_input(self):
        """Handle player input and update direction vector"""
        keys = pygame.key.get_pressed()

        # Reset direction vector
        self.direction.x = 0
        self.direction.y = 0

        # Calculate direction using boolean arithmetic
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        # Normalize diagonal movement
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

    def _move_axis(self, axis, dt):
        """Move along a specific axis and handle collisions"""
        direction_key = 'horizontal' if axis == 'x' else 'vertical'
        attr, center_attr, neg_side, pos_side = self.DIRECTIONS[direction_key]

        # Move collision rect
        setattr(self.collision_rect, attr,
                getattr(self.collision_rect, attr) + getattr(self.direction, attr) * self.SPEED * dt)

        # Handle collisions
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.collision_rect):
                direction_value = getattr(self.direction, attr)
                if direction_value > 0:  # Moving positive direction
                    setattr(self.collision_rect, pos_side, getattr(sprite.rect, neg_side))
                elif direction_value < 0:  # Moving negative direction
                    setattr(self.collision_rect, neg_side, getattr(sprite.rect, pos_side))

        # Sync render rect with collision rect
        setattr(self.rect, center_attr, getattr(self.collision_rect, center_attr))

    def _move(self, dt):
        """Handle player movement with collision detection"""
        self._move_axis('x', dt)
        self._move_axis('y', dt)

    def _animate(self, dt):
        """Update animation state and frame"""
        # Determine animation state based on movement
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        elif self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        # Update animation frame
        if self.direction.length() > 0:
            self.frame_index += self.ANIMATION_SPEED * dt
        else:
            self.frame_index = 0

        # Set current image
        frames = self.frames[self.state]
        self.image = frames[int(self.frame_index) % len(frames)]

    def update(self, dt):
        self._get_input()
        self._move(dt)
        self._animate(dt)