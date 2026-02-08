from pydantic import BaseModel, Field, field_validator
from typing import List, Dict
from enum import Enum


class BestPriceRequest(BaseModel):
    from_currency: str 
    to_currency: str

class BestPriceRaw(BaseModel):
    symbol: str
    timestamp: str
    price: float
    bid_inclusive_of_sell_spread: float
    sell_spread: float
    ask_inclusive_of_buy_spread: float
    buy_spread: float
    
class BestPriceResponse(BaseModel):
    results: List[BestPriceRaw]

#######################################################################

class Side(str, Enum):
    BID = "bid"
    ASK = "ask"
    BOTH = "both"

class BestPriceEstimatedRequest(BaseModel):
    from_currency: str 
    to_currency: str
    side: Side
    quantity: str

class BestPriceEstimatedRaw(BaseModel):
    symbol: str
    side: Side
    timestamp: str
    price: float
    bid_inclusive_of_sell_spread: float
    sell_spread: float
    ask_inclusive_of_buy_spread: float
    buy_spread: float

class BestPriceEstimatedResponse(BaseModel):
    results: List[BestPriceEstimatedRaw]
    