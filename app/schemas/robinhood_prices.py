from pydantic import BaseModel, Field, field_validator
from typing import List, Dict
from enum import Enum


class BestPriceRequest(BaseModel):
    from_currency: str 
    to_currency: str

class BestPriceRaw(BaseModel):
    symbol: str = Field(examples=["DOGE-USD"])
    timestamp: str = Field(examples=["2026-02-04T15:45:48.825787513Z"])
    price: int = Field(examples=["0.10367123"])
    bid_inclusive_of_sell_spread: int = Field(examples=["0.10279258"])
    sell_spread: int = Field(examples=["0.00847535"])
    ask_inclusive_of_buy_spread: int = Field(examples=["0.10454988"])
    buy_spread: int = Field(examples=["0.00847535"])

class BestPriceResponse(BaseModel):
    resutls: List[BestPriceRaw]

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
    symbol: str = Field(examples=["DOGE-USD"])
    side: Side
    timestamp: str = Field(examples=["2026-02-04T15:45:48.825787513Z"])
    price: int = Field(examples=["0.10367123"])
    bid_inclusive_of_sell_spread: int = Field(examples=["0.10279258"])
    sell_spread: int = Field(examples=["0.00847535"])
    ask_inclusive_of_buy_spread: int = Field(examples=["0.10454988"])
    buy_spread: int = Field(examples=["0.00847535"])

class BestPriceEstimatedResponse(BaseModel):
    resutls: List[BestPriceEstimatedRaw]
    