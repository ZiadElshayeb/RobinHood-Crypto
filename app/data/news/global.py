import requests
import os
from dotenv import load_dotenv
from app.schemas.global_news import GlobalNewsRequest, GlobalNewsResponse

load_dotenv()

class GlobalNews:
    BASE_URL = "https://eventregistry.org/api/v1/article"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.api_key = os.getenv("NEWS_AI_API_KEY")

    def get_articles(self, request: GlobalNewsRequest) -> str:
        url = f"{self.BASE_URL}/getArticles"
        
        if self.api_key is None:
            raise ValueError("NEWS_AI_API_KEY environment variable is not set")
        request.apiKey = self.api_key
        
        payload = request.model_dump(exclude_none=True)
        
        response = self.session.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        news_response = GlobalNewsResponse(**data)
        
        return news_response.model_dump_json(indent=2)
    
    def close(self):
        self.session.close()

# if __name__ == "__main__":
#     client = GlobalNews()
    
#     try:
#         print("--- Global News Search: Tesla Inc ---")
#         news_request = GlobalNewsRequest(
#             keyword="Tesla Inc",
#             ignoreSourceGroupUri="paywall/paywalled_sources",
#             articlesPage=1,
#             articlesCount=10,
#             articlesSortBy="date",
#             articlesSortByAsc=False,
#             dataType=["news", "pr"],
#             forceMaxDataTimeWindow=31,
#             apiKey=""  
#         )
        
#         news = client.get_articles(news_request)
#         print(news)
        
#     except requests.RequestException as e:
#         print(f"API Error: {e}")
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         client.close()
