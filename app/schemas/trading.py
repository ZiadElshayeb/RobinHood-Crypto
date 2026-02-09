from pydantic import BaseModel, Field
from typing import Optional

class MarketOrderConfig(BaseModel):
    asset_quantity: Optional[float] = Field(default=None, description="Asset quantity for market order.")

class LimitOrderConfig(BaseModel):
    quote_amount: Optional[float] = Field(default=None, description="Quote amount for limit order.")
    asset_quantity: Optional[float] = Field(default=None, description="Asset quantity for limit order.")
    limit_price: float = Field(description="Limit price for the order.")

class StopLossOrderConfig(BaseModel):
    quote_amount: Optional[float] = Field(default=None, description="Quote amount for stop loss order.")
    asset_quantity: Optional[float] = Field(default=None, description="Asset quantity for stop loss order.")
    stop_price: float = Field(description="Stop price for the order.")
    time_in_force: str = Field(default="gtc", description="Time in force (e.g., gtc, ioc, fok).")

class StopLimitOrderConfig(BaseModel):
    quote_amount: Optional[float] = Field(default=None, description="Quote amount for stop limit order.")
    asset_quantity: Optional[float] = Field(default=None, description="Asset quantity for stop limit order.")
    limit_price: float = Field(description="Limit price for the order.")
    stop_price: float = Field(description="Stop price for the order.")
    time_in_force: str = Field(default="gtc", description="Time in force (e.g., gtc, ioc, fok).")

class PlaceOrderRequest(BaseModel):
    symbol: str = Field(description="Currency pair symbol (e.g., BTC, ETH, DOGE).", examples=["BTC"])
    percentage: Optional[float] = Field(default=None, description="Percentage of holdings to trade.")
    quantity: Optional[float] = Field(default=None, description="Quantity to trade.")
    side: str = Field(description="Buy or sell.", examples=["buy", "sell"])

class OrderExecution(BaseModel):
    effective_price: str = Field(description="Effective price of execution.")
    quantity: str = Field(description="Quantity executed.")
    timestamp: str = Field(description="Timestamp of execution.")

class PlaceOrderResponse(BaseModel):
    id: str = Field(description="Order ID.")
    account_number: str = Field(description="Account number.")
    symbol: str = Field(description="Currency pair symbol.")
    client_order_id: str = Field(description="Client order ID.")
    side: str = Field(description="Buy or sell.")
    executions: list[OrderExecution] = Field(description="List of order executions.")
    type: str = Field(description="Type of order.")
    state: str = Field(description="Order state (e.g., open, filled, cancelled).")
    average_price: Optional[float] = Field(default=None, description="Average execution price.")
    filled_asset_quantity: Optional[float] = Field(default=None, description="Filled asset quantity.")
    created_at: str = Field(description="Creation timestamp.")
    updated_at: str = Field(description="Update timestamp.")
    market_order_config: Optional[MarketOrderConfig] = Field(default=None, description="Market order configuration.")
    limit_order_config: Optional[LimitOrderConfig] = Field(default=None, description="Limit order configuration.")
    stop_loss_order_config: Optional[StopLossOrderConfig] = Field(default=None, description="Stop loss order configuration.")
    stop_limit_order_config: Optional[StopLimitOrderConfig] = Field(default=None, description="Stop limit order configuration.")

class CancelOrderRequest(BaseModel):
    order_id: str = Field(description="ID of the order to cancel.")

class CancelOrderResponse(BaseModel):
    outcome: str = Field(description="Outcome of the cancellation request (e.g., success, failure).")
