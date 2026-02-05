import requests
from app.schemas.crypto_news import CryptoNewsRequest, CryptoNewsResponse

class CryptoNews:
    BASE_URL = "https://data-api.coindesk.com/news/v1"

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-type": "application/json; charset=UTF-8"})

    def search_news(self, request: CryptoNewsRequest) -> str:
        url = f"{self.BASE_URL}/search"
        params = {
            "lang": request.lang,
            "source_key": request.source_key,
            "search_string": request.search_string,
            "limit": request.limit
        }
        
        if request.to_ts != -1:
            params["to_ts"] = request.to_ts
        
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        news_response = CryptoNewsResponse(**data)
        
        return news_response.model_dump_json(indent=2)
    
    def close(self):
        self.session.close()

# if __name__ == "__main__":
#     client = CryptoNews()
    
#     try:
#         print("--- Crypto News Search: DOGE ---")
#         news_request = CryptoNewsRequest(
#             search_string="DOGE crypto",
#             limit=3,
#             lang="EN",
#             source_key="coindesk",
#             to_ts=-1
#         )
#         news = client.search_news(news_request)
#         print(news)
        
#     except requests.RequestException as e:
#         print(f"API Error: {e}")
#     finally:
#         client.close()
