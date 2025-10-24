import pygame
import sys
from libraries_and_settings import display_surface, WINDOW_WIDTH, WINDOW_HEIGHT
from words_library import instructions, trade, items

pygame.init()


class Menu:
    def __init__(self):
        self.running = True
        self.display_surface = display_surface
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)

    def draw_text_block(self, lines, start_y, spacing=40):
        """Draw multiple lines of text with automatic spacing"""
        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, 'white')
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, start_y + i * spacing))
            self.display_surface.blit(text_surf, text_rect)

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

            self.display_surface.fill('black')

            # Title
            title = self.title_font.render("GAME GUIDE", True, 'yellow')
            self.display_surface.blit(title, title.get_rect(center=(WINDOW_WIDTH // 2, 50)))

            # Display sections
            self.draw_text_block(instructions, 120)
            self.draw_text_block(trade, 240)
            self.draw_text_block(items, 400)

            pygame.display.update()


if __name__ == '__main__':
    screen = Menu()
    screen.run()