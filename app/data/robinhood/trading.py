import requests
from app.schemas.trading import PlaceOrderRequest, PlaceOrderResponse, CancelOrderRequest, CancelOrderResponse
from app.config import settings

class RobinhoodTrading:
    BASE_URL = settings.ROBINHOOD_BASE_URL

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()

    def place_order(self, request: PlaceOrderRequest) -> PlaceOrderResponse:
        url = f"{self.BASE_URL}/place/order"
        payload = request.model_dump(exclude_none=True)
        
        response = self.session.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        return PlaceOrderResponse(**data)
    
    def cancel_order(self, request: CancelOrderRequest) -> CancelOrderResponse:
        url = f"{self.BASE_URL}/cancel/order"
        payload = request.model_dump()
        
        response = self.session.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        
        return CancelOrderResponse(**data)
    
    def close(self):
        self.session.close()

# if __name__ == "__main__":
#     client = RobinhoodTrading()
#     try:
#         # Example: Sell 10% of DOGE holdings
#         order_request = PlaceOrderRequest(
#             symbol="DOGE",
#             percentage=10,
#             side="sell"
#         )
#         order = client.place_order(order_request)
#         print(order)
        
#         # Example: Cancel an order
#         cancel_request = CancelOrderRequest(
#             order_id="6769d103-07f4-423a-a794-1869a2bfa725"
#         )
#         cancel_response = client.cancel_order(cancel_request)
#         print(cancel_response)
        
#         # Example: Buy 0.05 BTC
#         order_request2 = PlaceOrderRequest(
#             symbol="BTC",
#             quantity=0.05,
#             side="buy"
#         )
#         order2 = client.place_order(order_request2)
#         print(order2)
        
#     except requests.RequestException as e:
#         print(f"API Error: {e}")
#     finally:
#         client.close()
