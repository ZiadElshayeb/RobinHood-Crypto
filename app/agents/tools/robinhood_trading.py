from agents import function_tool
from app.schemas.trading import PlaceOrderRequest, PlaceOrderResponse, CancelOrderRequest, CancelOrderResponse
from app.config import settings
import httpx

@function_tool
async def place_crypto_order(request: PlaceOrderRequest) -> PlaceOrderResponse:
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{settings.ROBINHOOD_BASE_URL}/place/order"
        payload = request.model_dump(exclude_none=True)
        
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        order_response = PlaceOrderResponse(**data)
        return order_response
    
@function_tool
async def cancel_crypto_order(request: CancelOrderRequest) -> CancelOrderResponse:
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{settings.ROBINHOOD_BASE_URL}/cancel/order"
        payload = request.model_dump()
        
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        cancel_response = CancelOrderResponse(**data)
        return cancel_response
