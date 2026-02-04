import requests
import json
from datetime import datetime

from app.schemas.market_data import Kline, TickerPrice

base_url = "https://api.binance.com/api/v3"

def get_klines(input: Kline, url: str = base_url) -> str:
    params = {
        "symbol": input.symbol,
        "interval": input.interval,
    }
    kline_response = requests.get(
        url=url + "/klines",
        params=params
    )

    output_klines = str(f"{'Open Time':<20} {'Open':<15} {'High':<15} {'Low':<15} {'Close':<15} {'Volume':<12} {'Close Time':<20} {'Quote Vol':<15} {'Trades':<10} {'Taker Buy Base':<15} {'Taker Buy Quote':<15}\n" +
    '='*180 + '\n')
    print(f"{'Open Time':<20} {'Open':<15} {'High':<15} {'Low':<15} {'Close':<15} {'Volume':<12} {'Close Time':<20} {'Quote Vol':<15} {'Trades':<10} {'Taker Buy Base':<15} {'Taker Buy Quote':<15}")
    print('='*180)

    for kline in kline_response.json()[:3]:
        open_time = datetime.fromtimestamp(kline[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        close_time = datetime.fromtimestamp(kline[6] / 1000).strftime('%Y-%m-%d %H:%M:%S')

        line = f"{open_time:<20} {kline[1]:<12} {kline[2]:<12} {kline[3]:<12} {kline[4]:<12} {kline[5]:<15} {close_time:<20} {kline[7]:<15} {kline[8]:<8} {kline[9]:<15} {kline[10]:<15}\n"
        output_klines += line
    return output_klines

def get_ticker_price(input: TickerPrice, url: str = base_url):
    params = {
        "symbol": input.symbol
    }
    response = requests.get(
        url=url + "/ticker/24hr",
        params=params
    )
    return response.json()

def main():
    # Create a Kline object, not a dictionary
    inputs = TickerPrice(
        symbol='btcusdt'
    )
    print(get_ticker_price(inputs))

if __name__ == "__main__":
    main()
