from alpaca_trade_api.rest import REST
import time

API_KEY = '(removed)'
API_SECRET = '(removed)'
BASE_URL = "https://paper-api.alpaca.markets"

alpaca = REST(API_KEY, API_SECRET, BASE_URL)
ticker_symbol = "AAPL"


try:
    while True:
        quote = alpaca.get_latest_trade(ticker_symbol)
        price = quote.price

        print(f"Current {ticker_symbol} price: ${price:.2f}")

        time.sleep(1) # 1 Second Delay
except KeyboardInterrupt:
    print("Stopped Live Updates.")
