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
SCROLL_SPEED = 1 # pixels per frame
SCALE = 3 # scale each font pixel to SCALExSCALE
CHAR_SPACING = 1 # blank columns between characters
TICKER_GAP = 8 # columns between tickers


COLOR_DEFAULT = (255, 255, 255)
COLOR_UP = (0, 255, 0)
COLOR_DOWN = (255, 0, 0)
BG_COLOR = (10, 10, 10)


# FONT utilities
def scale_char_matrix(char, scale=SCALE):
   # return list of rows (each row is list of ints 0/1) for scaled char_map
   pattern = FONT.get(char.upper(), FONT.get(" ", []))
   rows = len(pattern)
   cols = len(pattern[0]) if rows else 0
   # create scaled matrix rows*scale x cols*scale
   scaled = [[0] * (cols * scale) for _ in range(rows * scale)]
   for r, row in enumerate(pattern):
       for c, ch in enumerate(row):
           if ch == "1":
               for rr in range(scale):
                   for cc in range(scale):
                       scaled[r*scale + rr][c*scale + cc] = 1
   return scaled  # height = rows*scale


def vertical_centered_columns(char_matrix, total_rows):
   # char_matrix: list of rows, each row is list of ints, height = h
   h = len(char_matrix)
   if h == 0:
       return []
   cols = len(char_matrix[0])
   top_pad = (total_rows - h) // 2
   cols_out = []
   for c in range(cols):
       col = []
       for r in range(h):
           col.append(char_matrix[r][c])
       # add padding top and bottom to make column length == total_rows
       col = [0]*top_pad + col + [0]*(total_rows - top_pad - h)
       cols_out.append(col)
   return cols_out  # list of columns, each column is list of length total_rows


def text_to_pixel_columns(text):
   # Build a list of columns (each a list of length GRID_ROWS) for the whole text
   cols = []
   for ch in text:
       cm = scale_char_matrix(ch, SCALE)  # rows x cols
       ch_cols = vertical_centered_columns(cm, GRID_ROWS)
       cols.extend(ch_cols)
       # spacing columns between characters
       for _ in range(CHAR_SPACING):
           cols.append([0]*GRID_ROWS)
   return cols


# MAIN
def main():
   pygame.init()
   screen = pygame.display.set_mode((GRID_COLS*CELL_SIZE, GRID_ROWS*CELL_SIZE))
   pygame.display.set_caption("LED Stock Ticker")
   grid = Grid(GRID_ROWS, GRID_COLS, CELL_SIZE)
   clock = pygame.time.Clock()


   ticker_idx = 0
   # prepare first ticker pixel_map
   def build_ticker_text(ticker, price, direction):
       arrow = "↑" if direction == "up" else "↓" if direction == "down" else "-"
       # format: ARROW SPACE TICKER SPACE $PRICE (two decimals)
       if price is None:
           # if no price, show ticker only
           return f"{arrow} {ticker}"
       return f"{arrow} {ticker} ${price:.2f}"


   # initial fetch for all tickers to prime previous values
   last_prices = {}
   for t in TICKERS:
       p, d = get_price(t)
       last_prices[t] = p if p is not None else 0.0
       time.sleep(0.05)  # small pause to avoid hammering API


   current_ticker = TICKERS[ticker_idx]
   price, direction = get_price(current_ticker)
   if price is None:
       price = last_prices.get(current_ticker, 0.0)
       direction = "no_change"
   last_prices[current_ticker] = price
   text = build_ticker_text(current_ticker, price, direction)
   pixel_columns = text_to_pixel_columns(text)
   # add ticker gap columns after the ticker text
   for _ in range(TICKER_GAP):
       pixel_columns.append([0]*GRID_ROWS)


   offset = GRID_COLS  # how many columns off-screen to the right the text starts
   last_price_update = time.time()


   while True:
       for ev in pygame.event.get():
           if ev.type == pygame.QUIT:
               pygame.quit()
               sys.exit()


       # shift existing grid left one pixel
       for r in range(GRID_ROWS):
           for c in range(GRID_COLS - 1):
               grid.grid[r][c] = grid.grid[r][c+1]


       # which column from pixel_columns do we need to draw at right edge?
       col_index = -offset  # when offset == GRID_COLS -> col_index negative (no text yet)
       if 0 <= col_index < len(pixel_columns):
           col = pixel_columns[col_index]
       else:
           col = [0]*GRID_ROWS


       # choose color for lit pixels based on last seen direction for the current ticker
       # use last_prices comparison for direction
       last = last_prices.get(current_ticker, 0.0)
       # direction for coloring: if price increased since last stored value -> green, decreased -> red
       # We'll use the stored last value updated every 30s when we fetch new price.
       # For immediate coloring, default to white
       color_map = COLOR_DEFAULT
       # determine color from last diff (we don't want to call get_price here; color should correspond to
       # last_update-based direction stored in last_prices)
       # last_prices stores last price; we can compare against a prior value if we kept one,
       # but to keep simple: assume direction in the text we built
       # We'll parse the arrow character from the current text (first char)
       arrow_char = text[0] if len(text) > 0 else "-"
       if arrow_char == "↑":
           color_map = COLOR_UP
       elif arrow_char == "↓":
           color_map = COLOR_DOWN
       else:
           color_map = COLOR_DEFAULT


       # set right-most column pixels
       for r in range(GRID_ROWS):
           if col[r]:
               grid.grid[r][GRID_COLS-1] = color_map
           else:
               grid.grid[r][GRID_COLS-1] = BG_COLOR


       offset -= SCROLL_SPEED


       # every 30 seconds fetch price for the CURRENT ticker and rebuild pixel_columns (and arrow/color)
       if time.time() - last_price_update >= 30:
           # fetch fresh price
           price, direction = get_price(current_ticker)
           if price is None:
               price = last_prices.get(current_ticker, 0.0)
               direction = "no_change"
           # store last price for future comparisons
           last_prices[current_ticker] = price
           # rebuild displayed text for this ticker
           text = build_ticker_text(current_ticker, price, direction)
           pixel_columns = text_to_pixel_columns(text)
           for _ in range(TICKER_GAP):
               pixel_columns.append([0]*GRID_ROWS)
           # reset offset so the freshly updated ticker starts just off right edge
           offset = GRID_COLS
           last_price_update = time.time()


       # if the entire ticker scrolled off the left side, advance to next ticker
       if offset < -len(pixel_columns):
           # advance
           ticker_idx = (ticker_idx + 1) % len(TICKERS)
           current_ticker = TICKERS[ticker_idx]
           # prime next ticker: read last known price (non-blocking)
           price, direction = get_price(current_ticker)
           if price is None:
               price = last_prices.get(current_ticker, 0.0)
               direction = "no_change"
           last_prices[current_ticker] = price
           text = build_ticker_text(current_ticker, price, direction)
           pixel_columns = text_to_pixel_columns(text)
           for _ in range(TICKER_GAP):
               pixel_columns.append([0]*GRID_ROWS)
           offset = GRID_COLS
           last_price_update = time.time()


       # draw grid to screen
       grid.draw(screen)
       pygame.display.flip()
       clock.tick(30)




if __name__ == "__main__":
   main()
