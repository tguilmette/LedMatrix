# -----------------------------------------
# LED GRID SIMULATION (STATIC BLACK VERSION)
# -----------------------------------------

import pygame # Handles graphics, window, and drawing
import sys # For exiting the program cleanly

# ------------------------------
# CONFIGURATION
# ------------------------------
GRID_ROWS = 32 # Number of LED rows
GRID_COLS = 128 # Number of LED columns
CELL_SIZE = 10 # Pixel size of each LED on screen

WIDTH = GRID_COLS * CELL_SIZE # Total window width
HEIGHT = GRID_ROWS * CELL_SIZE # Total window height

LINE_COLOR = (50, 50, 50) # Grid line color (gray)
BG_COLOR = (10, 10, 10) # Background color (dark gray/black)
OFF_COLOR = (0, 0, 0) # LED "off" color (black)

# ------------------------------
# GRID CLASS
# ------------------------------
class Grid: # Defines how an object "Grid" is initialized
    def __init__(self, rows, cols, cell_size):
        # Create a grid of LEDs
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.width = cols * cell_size
        self.height = rows * cell_size

        # Create 2D list of black (off) LEDs
        # Essentially how this works is by iterating through the columns and setting the first cell to black
        # Then after doing this for the width, it iterated through each row doing the same
        self.grid = [[OFF_COLOR for _ in range(cols)] for _ in range(rows)]

    # Changes and LED's color by turning it on or off
    def set_pixel(self, row, col, color):
        if 0 <= row < self.rows and 0 <= col < self.cols: # LED is within grid boundaries
            self.grid[row][col] = color

    # Draw the full grid with LEDs and line
    def draw(self, screen):
        screen.fill(BG_COLOR)  # Clear screen first

        # Draw all LED squares
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

        # Draw horizontal grid lines
        for r in range(self.rows + 1):
            pygame.draw.line(
                screen,
                LINE_COLOR,
                (0, r * self.cell_size),
                (self.width, r * self.cell_size),
                1
            )

        # Draw vertical grid lines
        for c in range(self.cols + 1):
            pygame.draw.line(
                screen,
                LINE_COLOR,
                (c * self.cell_size, 0),
                (c * self.cell_size, self.height),
                1
            )

# ------------------------------
# MAIN PROGRAM
# ------------------------------
def main():
    pygame.init()  # Initialize Pygame

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("LED Grid Simulation - Static Black")

    grid = Grid(GRID_ROWS, GRID_COLS, CELL_SIZE)

    clock = pygame.time.Clock()
    running = True

    # ------------------------------
    # MAIN LOOP
    # ------------------------------
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Just draw the grid (no color changes)
        grid.draw(screen)
        pygame.display.flip()

        clock.tick(30)  # Limit frame rate to 30 FPS

    # ------------------------------
    # CLEANUP
    # ------------------------------
    pygame.quit()
    sys.exit()

# ------------------------------
# RUN PROGRAM
# ------------------------------
if __name__ == "__main__":
    main()
