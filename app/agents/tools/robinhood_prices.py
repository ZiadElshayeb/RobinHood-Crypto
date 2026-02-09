import httpx
from app.config import settings
from agents import function_tool
from app.schemas.robinhood_prices import BestPriceRequest, BestPriceResponse
BASE_URL = settings.ROBINHOOD_BASE_URL

@function_tool
async def get_best_price(inputs: BestPriceRequest) -> BestPriceResponse:

    json_body = {
        "from": inputs.from_currency,
        "to": inputs.to_currency
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=BASE_URL + '/getBestPrice',
            json=json_body
        )

    return BestPriceResponse(**response.json())
