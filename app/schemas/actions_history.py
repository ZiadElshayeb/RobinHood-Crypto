from pydantic import BaseModel, Field

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
    profit_loss: float = Field(description="The profit or loss from the action, if applicable.")