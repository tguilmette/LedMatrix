from alpaca_trade_api.rest import REST
import time

# API SETUP

API_KEY = "(REMOVED)"
API_SECRET = "(REMOVED)"
BASE_URL = "https://paper-api.alpaca.markets"

alpaca = REST(API_KEY, API_SECRET, BASE_URL)

# Stores previous price for each ticker
previous_prices = {}


# GET LATEST PRICE
def get_price(ticker):
    """Return (price, direction) using the latest Alpaca trade."""
    try:
        trade = alpaca.get_latest_trade(ticker)
        price = round(float(trade.price), 2)

        # Get the previous price if it exists
        prev_price = previous_prices.get(ticker, price)

        # Determine if price moved up, down, or stayed the same
        if price > prev_price:
            direction = "up"
        elif price < prev_price:
            direction = "down"
        else:
            direction = "no_change"

        # Save this price for next comparison
        previous_prices[ticker] = price
        return price, direction

    except Exception as e:
        # Print short error but let program continue
        print(f"Error getting price for {ticker}: {e}")
        return None, "no_change"

