Tim Guilmette
Computer Engineering Student @ UMass Amherst
Focused on fintech and software development.

# LedMatrix
# Stock Ticker Script

This Python script connects to the Alpaca Paper Trading API to display the latest stock price for a given ticker symbol. It also tracks price direction (whether the price is moving up, down, or unchanged) across updates.

Features:
1. Fetches real-time trade data from Alpaca’s paper trading environment.  
2. Tracks price direction (up, down, or no_change) for each symbol.  
3. Gracefully handles API errors without crashing the main loop.  
4. Designed to work both during and after market hours.

How It Works:
1. The script initializes a connection to Alpaca using your API key.
2. The get_price(ticker) function:
   - Retrieves the latest trade data.
   - Compares it to the previously stored price.
   - Returns both the current price and the direction of change.
3. The _prev dictionary stores previous prices so direction tracking works continuously.

Future Enhancements:
1. Expand the timeline of data (i.e. after close data shows change by comparing to previous date)
2. Plotting data / charts on simulation
3. Hardware component -- Real LED Board!!
4. Impliment other API (i.e. weather, sports ticker, follower count etc.) 


