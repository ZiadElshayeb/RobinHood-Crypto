from pydantic import BaseModel

class BookTickerRequest(BaseModel):
    symbol: str

class OrderBookRequest(BaseModel):
    symbol: str
    limit: int = 20
