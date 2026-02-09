from agents import function_tool
from app.schemas.crypto_news import CryptoNewsRequest, CryptoNewsResponse
import httpx

BASE_URL = "https://data-api.coindesk.com/news/v1"

@function_tool
async def search_crypto_news(request: CryptoNewsRequest) -> CryptoNewsResponse:
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{BASE_URL}/search"
        params = {
            "lang": request.lang,
            "source_key": request.source_key,
            "search_string": request.search_string,
            "limit": request.limit
        }
        
        if request.to_ts != -1:
            params["to_ts"] = request.to_ts
        
        response = await client.get(url, params=params, headers={"Content-type": "application/json; charset=UTF-8"})
        response.raise_for_status()
        data = response.json()
        
        news_response = CryptoNewsResponse(**data)
        
        return news_response
