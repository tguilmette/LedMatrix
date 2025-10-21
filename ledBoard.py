# ledBoard.py
import pygame

LINE_COLOR = (50, 50, 50)
BG_COLOR = (10, 10, 10)
OFF_COLOR = (0, 0, 0)

class Grid:
    def __init__(self, rows, cols, cell_size):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size
        # grid stores RGB tuples for each LED
        self.grid = [[OFF_COLOR for _ in range(cols)] for _ in range(rows)]

    def set_pixel(self, row, col, color):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = color

    def draw(self, screen):
        screen.fill(BG_COLOR)
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.grid[r][c]
                rect = pygame.Rect(
                    c * self.cell_size,
                    r * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, color, rect)

        # grid lines
        for r in range(self.rows + 1):
            pygame.draw.line(screen, LINE_COLOR, (0, r * self.cell_size), (self.width, r * self.cell_size), 1)
        for c in range(self.cols + 1):
            pygame.draw.line(screen, LINE_COLOR, (c * self.cell_size, 0), (c * self.cell_size, self.height), 1)

