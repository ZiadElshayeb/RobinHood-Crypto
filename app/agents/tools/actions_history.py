import datetime
from agents import function_tool
from app.database.database_class import Database
from app.schemas.actions_history import ActionsHistoryData, ToolsRequest

@function_tool
async def log_action(
    symbol: str,
    side: str,
    price: float,
    reason: str,
    quantity: float = 0.0,
    amount_usd: float = 0.0,
    profit_loss: float = 0.0
) -> str:
    """
    Log a trading decision (buy/sell/hold) to the database.
    
    Args:
        symbol: Crypto symbol (e.g., "DOGE", "BTC")
        side: Decision type - "buy", "sell", or "hold"
        price: Current price of the asset
        reason: Detailed explanation for the decision
        quantity: Quantity involved (default 0.0 for analysis)
        amount_usd: USD amount (default 0.0 for analysis)
        profit_loss: P/L if applicable (default 0.0)
    
    Returns:
        Confirmation message
    """
    db = Database()
    
    query = """
    INSERT INTO crypto_trade_history (symbol, side, quantity, price, amount_usd, reason, is_open, profit_loss)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    await db.insert_row(
        query,
        (
            symbol,
            side.lower(),  # Normalize to lowercase
            quantity,
            price,
            amount_usd,
            reason,
            True if side.lower() in ['buy', 'sell'] else False,  # Hold is not open position
            profit_loss
        )
    )
    
    return f"✓ Decision logged: {side.upper()} {symbol} at ${price:.4f} - {reason[:100]}"

@function_tool
async def get_recent_actions(limit: int = 10) -> list[dict]:
    db = Database()

    limit = max(1, min(int(limit), 100))

    query = """
    SELECT id, symbol, side, quantity, price, amount_usd, timestamp, reason, is_open, profit_loss
    FROM crypto_trade_history
    ORDER BY timestamp DESC
    LIMIT %s
    """

    rows = await db.fetch_all(query, (limit,))

    columns = [
        "id", "symbol", "side", "quantity", "price", "amount_usd",
        "timestamp", "reason", "is_open", "profit_loss"
    ]

    result: list[dict] = []
    for row in rows:
        d = dict(zip(columns, row))

        ts = d.get("timestamp")
        if isinstance(ts, datetime.datetime):
            d["timestamp"] = ts.isoformat()

        # validate/normalize with Pydantic, then return as plain dict (JSON-safe)
        result.append(ActionsHistoryData(**d).model_dump())

    return result

@function_tool
async def update_action_status(action_id: int, is_open: bool, profit_loss: float):
    db = Database()
    
    query = """
    UPDATE crypto_trade_history
    SET is_open = %s, profit_loss = %s
    WHERE id = %s
    """
    
    await db.update_row(query, (is_open, profit_loss, action_id))

@function_tool
async def log_tool_results(
    request: ToolsRequest
) -> str:
    db = Database()

    # Coerce numerics defensively (handles str/Decimal)
    step1_price_usd = float(request.step1_price_usd)
    step1_change_24h_pct = float(request.step1_change_24h_pct)
    step5_holdings_value_usd = float(request.step5_holdings_value_usd)
    side = (request.side or "").lower().strip()

    query = """
    INSERT INTO crypto_tools_result (
        step1_price_usd, step1_change_24h_pct, step2_order_book_signal,
        step3_candle_trend, step4_news_sentiment, step5_holdings_value_usd, side
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    await db.insert_row(
        query,
        (
            step1_price_usd,
            step1_change_24h_pct,
            request.step2_order_book_signal,
            request.step3_candle_trend,
            request.step4_news_sentiment,
            step5_holdings_value_usd,
            side,
        ),
    )

    return "✓ Tool results logged successfully."