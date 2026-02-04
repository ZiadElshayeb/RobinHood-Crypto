import requests
from app.schemas.binance_order_book import BookTickerRequest, OrderBookRequest

class BinanceOrderBook:
    BASE_URL = "https://api.binance.com"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()

    def get_best_ticker(self, request: BookTickerRequest) -> dict:
        url = f"{self.BASE_URL}/api/v3/ticker/bookTicker"
        response = self.session.get(url, params={"symbol": request.symbol}, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        bid = float(data['bidPrice'])
        ask = float(data['askPrice'])
        spread = ask - bid
        spread_bps = (spread / ((ask + bid) / 2)) * 10_000 if (ask + bid) > 0 else 0
        bid_qty = float(data['bidQty'])
        ask_qty = float(data['askQty'])

        return {
            "symbol": request.symbol,
            "type": "bookTicker",
            "bid_price": bid,
            "ask_price": ask,
            "spread": spread,
            "spread_bps": spread_bps,
            "bid_quantity": bid_qty,
            "ask_quantity": ask_qty
        }
    
    def get_order_book(self, request: OrderBookRequest) -> dict:
        url = f"{self.BASE_URL}/api/v3/depth"
        response = self.session.get(url, params={"symbol": request.symbol, "limit": request.limit}, timeout=self.timeout)
        response.raise_for_status()
        book = response.json()

        best_bid = float(book["bids"][0][0]) if book["bids"] else 0.0
        best_ask = float(book["asks"][0][0]) if book["asks"] else 0.0

        bids = [ float(p) for p, _ in book["bids"]]
        asks = [ float(p) for p, _ in book["asks"]]

        bids_qty = [ float(q) for _, q in book["bids"]]
        asks_qty = [ float(q) for _, q in book["asks"]]
        
        return {
            "symbol": request.symbol,
            "type": "depth",
            "best_bid": best_bid,
            "best_ask": best_ask,
            "spread": best_ask - best_bid,
            "bids": bids,
            "bids_qty": bids_qty,
            "asks": asks,
            "asks_qty": asks_qty,
            "limit": request.limit,
            "last_update_id": book["lastUpdateId"]
        }
    
    def close(self):
        self.session.close()

# if __name__ == "__main__":
#     client = BinanceOrderBook()
#     symbol = "DOGEUSDT"
    
#     try:
#         print(f"--- Best Ticker for {symbol} ---")
#         print(client.get_best_ticker(BookTickerRequest(symbol=symbol)))
#         print()

#         print(f"--- Order Book Depth (Limit=10) for {symbol} ---")
#         print(client.get_order_book(OrderBookRequest(symbol=symbol, limit=10)))
        
#     except requests.RequestException as e:
#         print(f"API Error: {e}")
#     finally:
#         client.close()