# stockTicker.py
from alpaca_trade_api.rest import REST
import time

API_KEY = "(REMOVED)"
API_SECRET = "(REMOVED)"
BASE_URL = "https://paper-api.alpaca.markets"

alpaca = REST(API_KEY, API_SECRET, BASE_URL)

_prev = {}  # previous price per ticker for direction

def get_price(ticker):
    
    try:
        quote = alpaca.get_latest_trade(ticker)
        price = round(float(quote.price), 2)
        prev = _prev.get(ticker, price)
        if price > prev:
            direction = "up"
        elif price < prev:
            direction = "down"
        else:
            direction = "no_change"
        _prev[ticker] = price
        return price, direction
    except Exception as e:
        # print a concise error so you see problems but main can keep running
        print(f"stockTicker.get_price error for {ticker}: {e}")
        return None, "no_change"
