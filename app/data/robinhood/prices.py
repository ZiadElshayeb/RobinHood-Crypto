import requests
from app.config import settings
from app.schemas.robinhood_prices import BestPriceRequest, BestPriceResponse, BestPriceEstimatedRequest, BestPriceEstimatedResponse
BASE_URL = settings.ROBINHOOD_BASE_URL

def get_best_price(inputs: BestPriceRequest) -> BestPriceResponse:

    json_body = {
        "from": inputs.from_currency,
        "to": inputs.to_currency
    }
    response = requests.post(
        url=BASE_URL + '/getBestPrice',
        json=json_body
    )

    return BestPriceResponse(**response.json())


def get_estimated_price(inputs: BestPriceEstimatedRequest) -> BestPriceEstimatedResponse:

    json_body = {
        "from": inputs.from_currency,
        "to": inputs.to_currency
    }
    response = requests.post(
        url=BASE_URL + '/getEstimatedPrice',
        json=json_body
    )

    return BestPriceEstimatedResponse(**response.json())



def main():
    inputs = BestPriceRequest(
        from_currency="DOGE",
        to_currency="USD"
    )

    print(get_best_price(inputs))

if __name__ == "__main__":
    main()