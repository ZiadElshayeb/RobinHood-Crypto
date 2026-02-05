from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional

class Intervals(str, Enum):
    # seconds
    ONE_SECOND = '1s'
    
    # minutes
    ONE_MINUTE = '1m'
    THREE_MINUTES = '3m'
    FIVE_MINUTES = '5m'
    FIFTEEN_MINUTES = '15m'
    THIRTY_MINUTES = '30m'
    
    # hours
    ONE_HOUR = '1h'
    TWO_HOURS = '2h'
    FOUR_HOURS = '4h'
    SIX_HOURS = '6h'
    EIGHT_HOURS = '8h'
    TWELVE_HOURS = '12h'
    
    # days
    ONE_DAY = '1d'
    THREE_DAYS = '3d'
    
    # weeks
    ONE_WEEK = '1w'
    
    # months
    ONE_MONTH = '1M'

class Kline(BaseModel):
    symbol: str = Field()
    interval: Intervals
    startTime: Optional[int] = None
    endTime: Optional[int] = None
    timeZone: Optional[str] = "UTC"
    limit: Optional[int] = Field(default=500, gt=0, lt=1000)


    @field_validator('symbol')
    @classmethod
    def uppercase_symbol(cls, v):
        return v.upper()
    
class TickerPrice(BaseModel):
    symbol: str = Field()

    @field_validator('symbol')
    @classmethod
    def uppercase_symbol(cls, v):
        return v.upper()