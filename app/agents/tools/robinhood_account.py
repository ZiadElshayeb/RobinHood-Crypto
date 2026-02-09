from agents import function_tool
from app.schemas.robinhood_account_info import (
    RobinhoodCryptoOrdersRequest,
    RobinhoodAccountInfoResponse,
    RobinhoodCryptoHoldingsResponse,
    RobinhoodCryptoOrdersResponse,
    RobinhoodTradingPairsResponse,
    RobinhoodTradingPairsRequest
)
from app.config import settings
import httpx

@function_tool
async def get_account_info() -> RobinhoodAccountInfoResponse:
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{settings.ROBINHOOD_BASE_URL}/get-account"
        response = await client.post(url)
        response.raise_for_status()
        data = response.json()
        
        account_info = RobinhoodAccountInfoResponse(**data)
        return account_info

@function_tool
async def get_crypto_holdings() -> RobinhoodCryptoHoldingsResponse:
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{settings.ROBINHOOD_BASE_URL}/getCryptoHoldings"
        response = await client.post(url)
        response.raise_for_status()
        data = response.json()
        
        holdings = RobinhoodCryptoHoldingsResponse(**data)
        return holdings

@function_tool
async def get_crypto_orders(request: RobinhoodCryptoOrdersRequest) -> RobinhoodCryptoOrdersResponse:
     async with httpx.AsyncClient(timeout=10) as client:
        url = f"{settings.ROBINHOOD_BASE_URL}/getCryptoOrders?startDate={request.start_date}&endDate={request.end_date}&symbol={request.symbol}&type={request.type}"
        payload = {
            "start_date": request.start_date,
            "end_date": request.end_date,
            "symbol": request.symbol,
            "type": request.type
        }
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        orders = RobinhoodCryptoOrdersResponse(**data)
        return orders

@function_tool
async def get_trading_pairs(request: RobinhoodTradingPairsRequest) -> RobinhoodTradingPairsResponse:
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{settings.ROBINHOOD_BASE_URL}/getTradingPairs"
        response = await client.post(url, json=request.model_dump())
        response.raise_for_status()
        data = response.json()
        
        trading_pairs = RobinhoodTradingPairsResponse(**data)
        return trading_pairs
