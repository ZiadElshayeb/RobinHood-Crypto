from agents import function_tool
from app.schemas.global_news import GlobalNewsRequest, GlobalNewsResponse
from typing import Optional
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://eventregistry.org/api/v1/article"

@function_tool
async def search_global_news(request: GlobalNewsRequest) -> GlobalNewsResponse:
    api_key = os.getenv("NEWS_AI_API_KEY")
    if api_key is None:
        raise ValueError("NEWS_AI_API_KEY environment variable is not set")
    request.apiKey = api_key
    
    async with httpx.AsyncClient(timeout=30) as client:
        url = f"{BASE_URL}/getArticles"
        payload = request.model_dump(exclude_none=True)
        
        response = await client.post(url, json=payload, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        data = response.json()
        
        news_response = GlobalNewsResponse(**data)
        
        return news_response
