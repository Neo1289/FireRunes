import pygame
import sys

# Import your configurations
from libraries_and_settings import display_surface, WINDOW_WIDTH, WINDOW_HEIGHT

pygame.init()


class HiddenDoorScreen:
    def __init__(self):
        self.running = True
        self.display_surface = display_surface
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            # Fill screen with black
            self.display_surface.fill('black')

            pygame.display.update()


if __name__ == '__main__':
    screen = HiddenDoorScreen()
    screen.run()
