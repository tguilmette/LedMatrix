# display_controller.py
import pygame
from config import SCROLL_SPEED

GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

class TickerDisplay:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Courier", 24)
        self.x_pos = width

    def draw_text(self, text, color):
        surface = self.font.render(text, True, color)
        return surface

    def scroll_text(self, text_surface):
        self.screen.fill((0, 0, 0))
        self.screen.blit(text_surface, (self.x_pos, self.height // 2 - 10))
        pygame.display.flip()
        self.x_pos -= SCROLL_SPEED
        if self.x_pos < -text_surface.get_width():
            self.x_pos = self.width
