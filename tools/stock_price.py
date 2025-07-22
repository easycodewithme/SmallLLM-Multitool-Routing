import re
import yfinance as yf

def get_stock_price(text: str) -> str:
    # Improved: look for 'Apple' or 'AAPL' case-insensitively
    if "apple" in text.lower():
        ticker = "AAPL"
    else:
        # Try regex fallback for uppercase ticker
        match = re.search(r"\b[A-Z]{2,5}\b", text)
        ticker = match.group(0) if match else None

    if not ticker:
        return "❌ Could not find a valid stock ticker in the request."

    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get("regularMarketPrice", None)
        if price is None:
            return f"❌ No data found for ticker {ticker}."
        return f"The current stock price of {ticker} is ${price:.2f}."
    except Exception as e:
        return f"❌ Error fetching stock price: {str(e)}"
