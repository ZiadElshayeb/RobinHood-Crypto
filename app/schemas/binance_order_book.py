from pydantic import BaseModel

class BookTickerRequest(BaseModel):
    symbol: str

class OrderBookRequest(BaseModel):
    symbol: str
    limit: int = 20

class BookTickerResponse(BaseModel):
    symbol: str
    type: str
    bid_price: float
    ask_price: float
    spread: float
    spread_bps: float
    bid_quantity: float
    ask_quantity: float

class OrderBookResponse(BaseModel):
    symbol: str
    type: str
    best_bid: float
    best_ask: float
    spread: float
    bids: list[float]
    bids_qty: list[float]
    asks: list[float]
    asks_qty: list[float]
    limit: int
    last_update_id: int