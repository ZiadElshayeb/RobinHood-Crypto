from pydantic import BaseModel, Field

class KlineWebSocketRequest(BaseModel):
    symbol: str = Field(description="Currency pair symbol (e.g., BTC, ETH, DOGE).", examples=["BTCUSDT"])
    interval: str = Field(description="Kline interval (e.g., 1m, 5m, 1h).", examples=["1m", "5m", "1h"])

class KData(BaseModel):
   kline_start_time: int = Field(description="Kline start time.")
   kline_close_time: int = Field(description="Kline close time.")
   symbol: str = Field(description="Currency pair symbol.")
   interval: str = Field(description="Kline interval.")
   first_trade_id: int = Field(description="First trade ID.")
   last_trade_id: int = Field(description="Last trade ID.")
   open_price: str = Field(description="Open price.")
   close_price: str = Field(description="Close price.")
   high_price: str = Field(description="High price.")
   low_price: str = Field(description="Low price.")
   base_asset_volume: str = Field(description="Base asset volume.")
   number_of_trades: int = Field(description="Number of trades.")
   is_kline_closed: bool = Field(description="Whether the kline is closed.")
   quote_asset_volume: str = Field(description="Quote asset volume.")
   taker_buy_base_asset_volume: str = Field(description="Taker buy base asset volume.")
   taker_buy_quote_asset_volume: str = Field(description="Taker buy quote asset volume")
   ignore: str = Field(description="Ignored field.")

class KlineWebSocketResponse(BaseModel):
  event_type: str = Field(description="Event type.")
  event_time: int = Field(description="Event time.")
  symbol: str = Field(description="Currency pair symbol.")
  kline: KData = Field(description="Kline data.")