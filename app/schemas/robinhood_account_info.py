from pydantic import BaseModel, Field

class RobinhoodCryptoOrdersRequest(BaseModel):
    start_date: str = Field(examples=["2024-01-01"])
    end_date: str = Field(examples=["2024-12-31"])
    symbol: str = Field(examples=["BTC"])
    type: str = Field(examples=["market", "limit", "stop_loss", "stop_limit"])

class RobinhoodAccountInfoResponse(BaseModel):
    account_number: str = Field(examples=["123456789"])
    buying_power: str = Field(examples=["10000.00"])
    status: str = Field(examples=["active"])
    buying_power_currency: str = Field(examples=["USD"])

class RobinhoodCryptoHoldingsResultsItem(BaseModel):
    account_number: str = Field(examples=["123456789"])
    asset_code: str = Field(examples=["BTC"])
    total_quantity: str = Field(examples=["0.5"])
    quantity_available_for_trading: str = Field(examples=["0.3"])
    in_usd: str = Field(examples=["0.2"])

class RobinhoodCryptoHoldingsResponse(BaseModel):
    next: str | None = Field(examples=[None, "https://api.robinhood.com/crypto/holdings/?cursor=abc123"])
    previous: str | None = Field(examples=[None, "https://api.robinhood.com/crypto/holdings/?cursor=xyz789"])
    results: list[RobinhoodCryptoHoldingsResultsItem]

class RobinhoodCryptoOrdersExecutionItem(BaseModel):
    effective_price: str = Field(examples=["30000.00"])
    quantity: str = Field(examples=["0.1"])
    timestamp: str = Field(examples=["2024-01-15T12:40:00.456Z"])

class RobinhoodCryptoOrdersDataItem(BaseModel):
    symbol: str = Field(examples=["BTC"])
    client_order_id: str = Field(examples=["f2bb9706-a7e2-4242-b902-220acceccc46"])
    side: str = Field(examples=["buy", "sell"])
    type: str = Field(examples=["limit", "market"])
    account_number: str = Field(examples=["123456789"])
    id: str = Field(examples=["6769d103-07f4-423a-a794-1869a2bfa725"])
    state: str = Field(examples=["filled", "canceled"])
    filled_asset_quantity: str = Field(examples=["0.1"])
    average_price: str = Field(examples=["30000.00"])
    created_at: str = Field(examples=["2024-01-15T12:34:56.789Z"])
    updated_at: str = Field(examples=["2024-01-15T12:45:00.123Z"])
    executions: list[RobinhoodCryptoOrdersExecutionItem]
    market_order_config: dict = Field(examples=[{"quote_amount": "4,000"}])

class RobinhoodCryptoOrdersResponse(BaseModel):
    data: list[RobinhoodCryptoOrdersDataItem]

class RobinhoodTradingPairsRequest(BaseModel):
    from_currency: str = Field(examples=["BTC"])
    to_currency: str = Field(examples=["USD"])

class RobinhoodTradingPairsResultsItem(BaseModel):
    asset_code: str = Field(examples=["BTC"])
    quote_code: str = Field(examples=["USD"])
    max_order_size: str = Field(examples=["100"])
    min_order_size: str = Field(examples=["0.0001"])
    quote_increment: str = Field(examples=["0.01"])
    asset_increment: str = Field(examples=["0.00000001"])
    status: str = Field(examples=["active"])
    symbol: str = Field(examples=["BTC-USD"])

class RobinhoodTradingPairsResponse(BaseModel):
    next: str | None = Field(examples=[None, "https://api.robinhood.com/crypto/trading-pairs/?cursor=abc123"])
    previous: str | None = Field(examples=[None, "https://api.robinhood.com/crypto/trading-pairs/?cursor=xyz789"])
    results: list[RobinhoodTradingPairsResultsItem]