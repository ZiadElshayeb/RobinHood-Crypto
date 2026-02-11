from enum import Enum
from pydantic import BaseModel, Field

class CandleTrend(str, Enum):
    DOWN_TREND = "DownTrend"
    UP_TREND = "UpTrend"
    NEUTRAL = "Neutral"

class NewsSentiment(str, Enum):
    POSITIVE = "Positive"
    NEGATIVE = "Negative"
    NEUTRAL = "Neutral"
    MIXED = "Mixed"
    MIXED_NEGATIVE = "Mixed/Negative"
    MIXED_POSITIVE = "Mixed/Positive"

class ActionsHistoryData(BaseModel):
    id: int = Field(description="Unique identifier for the action history record.")
    symbol: str = Field(description="The symbol associated with the action (e.g., BTC, ETH).")
    side: str = Field(description="The side of the action (e.g., buy, sell).")
    quantity: float = Field(description="The quantity involved in the action.")
    price: float = Field(description="The price at which the action was executed.")
    amount_usd: float = Field(description="The total amount in USD for the action.")
    timestamp: str = Field(description="The timestamp when the action occurred.")
    reason: str = Field(description="The reason for the action (e.g., profit target hit, stop loss triggered).")
    is_open: bool = Field(description="Indicates whether the position is still open.") 

class ToolsRequest(BaseModel):
    step1_price_usd: float = Field(description="Price at step 1 (e.g., current price).")
    step1_change_24h_pct: float = Field(description="24-hour percentage change at step 1.")
    step2_order_book_signal: str = Field(description="Order book signal at step 2 (e.g., buy pressure, sell pressure).")
    step3_candle_trend: CandleTrend = Field(description="Candlestick pattern signal at step 3 (e.g., downtrend, uptrend, neutral).")
    step4_news_sentiment: NewsSentiment = Field(description="News sentiment at step 4 (e.g., positive, negative).")
    step5_holdings_value_usd: float = Field(description="Current holdings value in USD at step 5.")
    side: str = Field(description="The side of the action (e.g., buy, sell, hold).")

class ToolsResults(BaseModel):
    id: int = Field(description="Unique identifier for the tool result record.")
    step1_price_usd: float = Field(description="Price at step 1 (e.g., current price).")
    step1_change_24h_pct: float = Field(description="24-hour percentage change at step 1.")
    step2_order_book_signal: str = Field(description="Order book signal at step 2 (e.g., buy pressure, sell pressure).")
    step3_candle_trend: CandleTrend = Field(description="Candlestick pattern signal at step 3 (e.g., downtrend, uptrend, neutral).")
    step4_news_sentiment: NewsSentiment = Field(description="News sentiment at step 4 (e.g., positive, negative).")
    step5_holdings_value_usd: float = Field(description="Current holdings value in USD at step 5.")
    side: str = Field(description="The side of the action (e.g., buy, sell, hold).")