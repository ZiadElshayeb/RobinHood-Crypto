import requests
from app.schemas.robinhood_account_info import RobinhoodCryptoOrdersRequest, RobinhoodAccountInfoResponse, RobinhoodCryptoHoldingsResponse, RobinhoodCryptoOrdersResponse, RobinhoodTradingPairsResponse
from app.config import settings

class RobinhoodAccountInfo:
    BASE_URL = settings.ROBINHOOD_BASE_URL

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()

    def get_account_info(self) -> RobinhoodAccountInfoResponse:
        url = f"{self.BASE_URL}/get-account"
        response = self.session.post(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        return RobinhoodAccountInfoResponse(**data)
    
    def get_crypto_holdings(self) -> RobinhoodCryptoHoldingsResponse:
        url = f"{self.BASE_URL}/getCryptoHoldings"
        response = self.session.post(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        return RobinhoodCryptoHoldingsResponse(**data)
    
    def get_crypto_orders(self, request: RobinhoodCryptoOrdersRequest) -> RobinhoodCryptoOrdersResponse:
        url = f"{self.BASE_URL}/getCryptoOrders?startDate={request.start_date}&endDate={request.end_date}&symbol={request.symbol}&type={request.type}"
        payload = {
            "start_date": request.start_date,
            "end_date": request.end_date,
            "symbol": request.symbol,
            "type": request.type
        }
        response = self.session.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        return RobinhoodCryptoOrdersResponse(**data)
    
    def get_trading_pairs(self) -> RobinhoodTradingPairsResponse:
        url = f"{self.BASE_URL}/getTradingPairs"
        response = self.session.post(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        return RobinhoodTradingPairsResponse(**data)
    
    def close(self):
        self.session.close()

# if __name__ == "__main__":
#     client = RobinhoodAccountInfo()
#     try:
#         account_info = client.get_account_info()
#         print(account_info)
#         crypto_holdings = client.get_crypto_holdings()
#         print(crypto_holdings)
#         crypto_orders = client.get_crypto_orders(
#             RobinhoodCryptoOrdersRequest(
#                 start_date="2024-01-01",
#                 end_date="2024-12-31",
#                 symbol="DOGE",
#                 type="market"
#             )
#         )
#         print(crypto_orders)
#         trading_pairs = client.get_trading_pairs()
#         print(trading_pairs)
#     finally:
#         client.close()