import asyncio
import json
import websockets
from app.schemas.klines_websocket import KlineWebSocketRequest, KlineWebSocketResponse, KData


async def subscribe_kline_stream(request: KlineWebSocketRequest):
    symbol_lower = request.symbol.lower()
    url = f"wss://stream.binance.com:9443/ws/{symbol_lower}@kline_{request.interval}"
    
    async with websockets.connect(url) as websocket:
        async for message in websocket:
            try:
                data = json.loads(message)
                
                kline_data = KData(
                    kline_start_time=data["k"]["t"],
                    kline_close_time=data["k"]["T"],
                    symbol=data["k"]["s"],
                    interval=data["k"]["i"],
                    first_trade_id=data["k"]["f"],
                    last_trade_id=data["k"]["L"],
                    open_price=data["k"]["o"],
                    close_price=data["k"]["c"],
                    high_price=data["k"]["h"],
                    low_price=data["k"]["l"],
                    base_asset_volume=data["k"]["v"],
                    number_of_trades=data["k"]["n"],
                    is_kline_closed=data["k"]["x"],
                    quote_asset_volume=data["k"]["q"],
                    taker_buy_base_asset_volume=data["k"]["V"],
                    taker_buy_quote_asset_volume=data["k"]["Q"],
                    ignore=data["k"]["B"]
                )
                
                response = KlineWebSocketResponse(
                    event_type=data["e"],
                    event_time=data["E"],
                    symbol=data["s"],
                    kline=kline_data
                )
                
                yield response
                
            except (KeyError, json.JSONDecodeError) as e:
                print(f"Error parsing WebSocket message: {e}")
                continue


# if __name__ == "__main__":
#     async def main():
#         request = KlineWebSocketRequest(symbol="BTCUSDT", interval="1m")
        
#         print(f"Subscribing to {request.symbol} kline stream with {request.interval} interval...")
#         print("Press Ctrl+C to stop\n")
        
#         try:
#             async for kline_update in subscribe_kline_stream(request):
#                 print(f"Time: {kline_update.event_time}")
#                 print(f"Symbol: {kline_update.symbol}")
#                 print(f"Open: {kline_update.kline.open_price}")
#                 print(f"High: {kline_update.kline.high_price}")
#                 print(f"Low: {kline_update.kline.low_price}")
#                 print(f"Close: {kline_update.kline.close_price}")
#                 print(f"Volume: {kline_update.kline.base_asset_volume}")
#                 print(f"Closed: {kline_update.kline.is_kline_closed}")
#                 print("-" * 50)
#         except (KeyboardInterrupt, asyncio.CancelledError):
#             print("\n✓ Stream stopped successfully.")
    
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         pass
