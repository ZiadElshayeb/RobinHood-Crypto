from agents import function_tool
from app.schemas.binance_order_book import BookTickerRequest, BookTickerResponse, OrderBookRequest, OrderBookResponse
import httpx

BASE_URL = "https://api.binance.com"

@function_tool
async def get_best_ticker(request: BookTickerRequest) -> BookTickerResponse:    
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{BASE_URL}/api/v3/ticker/bookTicker"
        response = await client.get(url, params={"symbol": request.symbol})
        response.raise_for_status()
        data = response.json()

        bid = float(data['bidPrice'])
        ask = float(data['askPrice'])
        spread = ask - bid
        spread_bps = (spread / ((ask + bid) / 2)) * 10_000 if (ask + bid) > 0 else 0
        bid_qty = float(data['bidQty'])
        ask_qty = float(data['askQty'])

        return BookTickerResponse(
            symbol=request.symbol,
            type="bookTicker",
            bid_price=bid,
            ask_price=ask,
            spread=spread,
            spread_bps=spread_bps,
            bid_quantity=bid_qty,
            ask_quantity=ask_qty
        )

@function_tool
async def get_order_book(request: OrderBookRequest) -> OrderBookResponse:
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{BASE_URL}/api/v3/depth"
        response = await client.get(url, params={"symbol": request.symbol, "limit": request.limit})
        response.raise_for_status()
        book = response.json()

        best_bid = float(book["bids"][0][0]) if book["bids"] else 0.0
        best_ask = float(book["asks"][0][0]) if book["asks"] else 0.0

        bids = [float(p) for p, _ in book["bids"]]
        asks = [float(p) for p, _ in book["asks"]]

        bids_qty = [float(q) for _, q in book["bids"]]
        asks_qty = [float(q) for _, q in book["asks"]]
        
        return OrderBookResponse(
            symbol=request.symbol,
            type="depth",
            best_bid=best_bid,
            best_ask=best_ask,
            spread=best_ask - best_bid,
            bids=bids,
            bids_qty=bids_qty,
            asks=asks,
            asks_qty=asks_qty,
            limit=request.limit,
            last_update_id=book["lastUpdateId"]
        )
