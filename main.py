# main.py
import pygame
import sys
import time
from characters import FONT
from stockTicker import get_price
from ledBoard import Grid

# CONFIG

GRID_ROWS = 32
GRID_COLS = 128
CELL_SIZE = 10

TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN"]
SCROLL_SPEED = 1
SCALE = 3
CHAR_SPACING = 1
TICKER_GAP = 8

COLOR_DEFAULT = (255, 255, 255)
COLOR_UP = (0, 255, 0)
COLOR_DOWN = (255, 0, 0)
BG_COLOR = (10, 10, 10)


# TEXT FUNCTIONS

def scale_char(char):
    pattern = FONT.get(char.upper(), FONT[" "])
    scaled = []
    for row in pattern:
        new_row = ""
        for ch in row:
            new_row += ch * SCALE
        for _ in range(SCALE):
            scaled.append(new_row)
    return [list(r) for r in scaled]


def make_columns(char_matrix):
    rows = len(char_matrix)
    cols = len(char_matrix[0])
    top_padding = (GRID_ROWS - rows) // 2

    columns = []
    for c in range(cols):
        col = [0] * GRID_ROWS
        for r in range(rows):
            if char_matrix[r][c] == "1":
                col[top_padding + r] = 1
        columns.append(col)
    return columns


def text_to_columns(text):
    all_columns = []
    for ch in text:
        scaled = scale_char(ch)
        columns = make_columns(scaled)
        all_columns.extend(columns)
        for _ in range(CHAR_SPACING):
            all_columns.append([0] * GRID_ROWS)
    return all_columns


# HELPER FUNCTIONS

def build_ticker_text(ticker, price, direction):
    if direction == "up":
        arrow = "↑"
    elif direction == "down":
        arrow = "↓"
    else:
        arrow = "-"
    if price is None:
        return f"{arrow} {ticker}"
    return f"{arrow} {ticker} ${price:.2f}"


def get_color_from_arrow(arrow):
    if arrow == "↑":
        return COLOR_UP
    elif arrow == "↓":
        return COLOR_DOWN
    return COLOR_DEFAULT


# MAIN LOOP

def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_COLS * CELL_SIZE, GRID_ROWS * CELL_SIZE))
    pygame.display.set_caption("LED Stock Ticker")
    grid = Grid(GRID_ROWS, GRID_COLS, CELL_SIZE)
    clock = pygame.time.Clock()

    # Initialize last known prices
    last_prices = {}
    for t in TICKERS:
        price, _ = get_price(t)
        last_prices[t] = price if price else 0.0
        time.sleep(0.05)

    ticker_index = 0
    current_ticker = TICKERS[ticker_index]

    # Get first price
    price, _ = get_price(current_ticker)
    if price is None:
        price = last_prices[current_ticker]
    last_prices[current_ticker] = price
    direction = "no_change"

    # Build text for first ticker
    text = build_ticker_text(current_ticker, price, direction)
    pixel_columns = text_to_columns(text)
    pixel_columns += [[0] * GRID_ROWS for _ in range(TICKER_GAP)]

    offset = GRID_COLS
    last_update = time.time()

    while True:
        # --- Handle Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Scroll Grid Left ---
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS - 1):
                grid.grid[r][c] = grid.grid[r][c + 1]

        # --- Determine Next Column ---
        col_index = -offset
        if 0 <= col_index < len(pixel_columns):
            next_col = pixel_columns[col_index]
        else:
            next_col = [0] * GRID_ROWS

        # --- Color Based on Arrow ---
        arrow = text[0] if text else "-"
        color = get_color_from_arrow(arrow)

        # --- Draw Rightmost Column ---
        for r in range(GRID_ROWS):
            grid.grid[r][GRID_COLS - 1] = color if next_col[r] else BG_COLOR

        offset -= SCROLL_SPEED

        # --- Update Price Every 30 Seconds ---
        if time.time() - last_update >= 30:
            new_price, _ = get_price(current_ticker)
            if new_price is None:
                new_price = last_prices[current_ticker]

            # Determine direction by comparing old and new price
            old_price = last_prices[current_ticker]
            if new_price > old_price:
                direction = "up"
            elif new_price < old_price:
                direction = "down"
            else:
                direction = "no_change"

            last_prices[current_ticker] = new_price
            price = new_price

            text = build_ticker_text(current_ticker, price, direction)
            pixel_columns = text_to_columns(text)
            pixel_columns += [[0] * GRID_ROWS for _ in range(TICKER_GAP)]

            offset = GRID_COLS
            last_update = time.time()

        # --- Switch to Next Ticker ---
        if offset < -len(pixel_columns):
            ticker_index = (ticker_index + 1) % len(TICKERS)
            current_ticker = TICKERS[ticker_index]
            new_price, _ = get_price(current_ticker)
            if new_price is None:
                new_price = last_prices[current_ticker]

            old_price = last_prices[current_ticker]
            if new_price > old_price:
                direction = "up"
            elif new_price < old_price:
                direction = "down"
            else:
                direction = "no_change"

            last_prices[current_ticker] = new_price
            price = new_price

            text = build_ticker_text(current_ticker, price, direction)
            pixel_columns = text_to_columns(text)
            pixel_columns += [[0] * GRID_ROWS for _ in range(TICKER_GAP)]

            offset = GRID_COLS
            last_update = time.time()

        # --- Draw Grid ---
        grid.draw(screen)
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main()
