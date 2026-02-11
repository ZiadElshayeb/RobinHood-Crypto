import httpx
from datetime import datetime
from agents import function_tool

BASE_URL = "https://api.binance.com/api/v3"

@function_tool
async def get_klines(symbol: str, interval: str = "1h", limit: int = 500) -> str:
    """Fetch kline/candlestick data from Binance. 
    symbol: trading pair e.g. BTCUSDT, DOGEUSDT. 
    interval: candle interval e.g. 1s,1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M. 
    limit: number of candles (1-1000)."""
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": min(max(limit, 1), 1000),
    }
    async with httpx.AsyncClient() as client:
        kline_response = await client.get(url=f"{BASE_URL}/klines", params=params)
        kline_response.raise_for_status()

    header = f"{'Open Time':<20} {'Open':<15} {'High':<15} {'Low':<15} {'Close':<15} {'Volume':<12} {'Close Time':<20} {'Quote Vol':<15} {'Trades':<10} {'Taker Buy Base':<15} {'Taker Buy Quote':<15}\n"
    output_klines = header + '=' * 180 + '\n'

    for kline in kline_response.json():
        open_time = datetime.fromtimestamp(kline[0] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        close_time = datetime.fromtimestamp(kline[6] / 1000).strftime('%Y-%m-%d %H:%M:%S')
        line = f"{open_time:<20} {kline[1]:<12} {kline[2]:<12} {kline[3]:<12} {kline[4]:<12} {kline[5]:<15} {close_time:<20} {kline[7]:<15} {kline[8]:<8} {kline[9]:<15} {kline[10]:<15}\n"
        output_klines += line
    return output_klines


@function_tool
async def get_ticker_price(symbol: str) -> str:
    """Get 24hr ticker price statistics for a symbol. symbol: e.g. BTCUSDT, DOGEUSDT."""
    params = {"symbol": symbol.upper()}
    async with httpx.AsyncClient() as client:
        response = await client.get(url=f"{BASE_URL}/ticker/24hr", params=params)
        response.raise_for_status()
    return str(response.json())