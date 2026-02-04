import requests
from app.schemas.binance_order_book import BookTickerRequest, OrderBookRequest

class BinanceOrderBook:
    BASE_URL = "https://api.binance.com"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()

    def get_best_ticker(self, request: BookTickerRequest) -> str:
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

        header = f"{'Symbol':<12} {'Type':<15} {'Bid':<15} {'Bid Qty':<15} {'Ask':<15} {'Ask Qty':<15} {'Spread':<15} {'Spread BPS':<12}"
        separator = "-" * 120
        data_row = f"{request.symbol:<12} {'bookTicker':<15} {bid:<15.8f} {bid_qty:<15.2f} {ask:<15.8f} {ask_qty:<15.2f} {spread:<15.8f} {spread_bps:<12.2f}"
        
        return f"{header}\n{separator}\n{data_row}"
    
    def get_order_book(self, request: OrderBookRequest) -> str:
        url = f"{self.BASE_URL}/api/v3/depth"
        response = self.session.get(url, params={"symbol": request.symbol, "limit": request.limit}, timeout=self.timeout)
        response.raise_for_status()
        book = response.json()

        bids = [(float(p), float(q)) for p, q in book["bids"]]
        asks = [(float(p), float(q)) for p, q in book["asks"]]
        
        bids_output = ["\nBIDS"]
        bids_output.append(f"{'Price':<15} {'Quantity':<15}")
        bids_output.append("-" * 30)
        for price, qty in bids:
            bids_output.append(f"{price:<15.8f} {qty:<15.2f}")
        
        asks_output = ["\nASKS"]
        asks_output.append(f"{'Price':<15} {'Quantity':<15}")
        asks_output.append("-" * 30)
        for price, qty in asks:
            asks_output.append(f"{price:<15.8f} {qty:<15.2f}")
        
        return "\n".join(bids_output + asks_output)
    
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