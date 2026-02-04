import requests
from typing import Dict, Union, List

class BinanceOrderBook:
    BASE_URL = "https://api.binance.com"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()

    def get_best_ticker(self, symbol: str) -> Dict[str, Union[str, float]]:
        url = f"{self.BASE_URL}/api/v3/ticker/bookTicker"
        response = self.session.get(url, params={"symbol": symbol}, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        bid = float(data['bidPrice'])
        ask = float(data['askPrice'])
        spread = ask - bid
        spread_bps = (spread / ((ask + bid) / 2)) * 10_000 if (ask + bid) > 0 else 0

        return {
            "symbol": symbol,
            "type": "bookTicker",
            "bid": bid,
            "bid_qty": float(data['bidQty']),
            "ask": ask,
            "ask_qty": float(data['askQty']),
            "spread": spread,
            "spread_bps": spread_bps
        }
    
    def get_order_book(self, symbol: str, limit: int = 20) -> Dict[str, Union[str, int, float, List]]:
        url = f"{self.BASE_URL}/api/v3/depth"
        response = self.session.get(url, params={"symbol": symbol, "limit": limit}, timeout=self.timeout)
        response.raise_for_status()
        book = response.json()

        best_bid = float(book["bids"][0][0]) if book["bids"] else 0.0
        best_ask = float(book["asks"][0][0]) if book["asks"] else 0.0
        
        return {
            "symbol": symbol,
            "type": "depth",
            "lastUpdateId": book.get("lastUpdateId"),
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread": best_ask - best_bid,
            "bids": [(float(p), float(q)) for p, q in book["bids"]],
            "asks": [(float(p), float(q)) for p, q in book["asks"]]
        }
    
    def close(self):
        self.session.close()

# if __name__ == "__main__":
#     client = BinanceOrderBook()
#     symbol = "DOGEUSDT"
    
#     try:
#         print(f"--- Fecthing Best Ticker for {symbol} ---")
#         ticker = client.get_best_ticker(symbol)
#         print(f"Bid: {ticker['bid']} | Ask: {ticker['ask']} | Spread bps: {ticker['spread_bps']:.2f}\n")

#         print(f"--- Fetching Depth (Limit=5) for {symbol} ---")
#         depth = client.get_order_book(symbol, limit=5)
#         print(f"Top 5 Bids: {depth['bids']}")
#         print(f"Top 5 Asks: {depth['asks']}")
        
#     except requests.RequestException as e:
#         print(f"API Error: {e}")
#     finally:
#         client.close()