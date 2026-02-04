from pydantic import BaseModel

class RobinhoodCryptoOrdersRequest(BaseModel):
    start_date: str
    end_date: str
    symbol: str
    type: str