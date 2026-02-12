from agents import (
    Agent,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    SQLiteSession,
    Tool,
)
from openai.types.responses import ResponseTextDeltaEvent
from app.config import settings
from openai import AsyncOpenAI
import asyncio
import sys
import json
import httpx
import logging
from datetime import datetime
import time

# Import all tools (excluding place and cancel order for safety)
from app.agents.tools.binance_market_data import get_klines, get_ticker_price
from app.agents.tools.binance_order_book import get_best_ticker, get_order_book
from app.agents.tools.crypto_news import search_crypto_news
from app.agents.tools.global_news import search_global_news
from app.agents.tools.robinhood_account import (
    get_account_info,
    get_crypto_holdings,
    get_crypto_orders,
    get_trading_pairs,
)
from app.agents.tools.robinhood_prices import get_best_price
from app.agents.tools.actions_history import get_recent_actions, log_action, log_tool_results

# Fix for Windows async compatibility
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# -----------------------------------------------------------------------------
# Silence HTTP URL logs (httpx/httpcore/openai/agents)
# -----------------------------------------------------------------------------
logging.basicConfig(level=logging.WARNING)

for name in (
    "httpx",
    "httpcore",
    "openai",
    "openai._base_client",
    "openai._utils",
    "agents",
):
    logging.getLogger(name).setLevel(logging.WARNING)

# As a safety net, prevent noisy INFO logs from propagating
logging.getLogger().setLevel(logging.WARNING)

# -----------------------------------------------------------------------------

BASE_URL = settings.GEMINI_BASE_URL
API_KEY = settings.GEMINI_API_KEY
MODEL_NAME = settings.GEMINI_MODEL

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError("Please set BASE_URL, API_KEY, MODEL_NAME via .env")

###############################################################################
# Custom httpx Transport that modifies requests before sending
###############################################################################
class SchemaCleaningTransport(httpx.AsyncHTTPTransport):
    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        original_request = request

        try:
            # Only attempt schema-cleaning when the outgoing body has tools
            if request.content and b'"tools"' in request.content:
                body_json = json.loads(request.content.decode("utf-8"))

                if isinstance(body_json, dict) and "tools" in body_json:
                    for tool in body_json["tools"]:
                        if "function" in tool and isinstance(tool["function"], dict):
                            func = tool["function"]

                            # Remove Gemini-incompatible fields
                            func.pop("strict", None)

                            params = func.get("parameters")
                            if isinstance(params, dict):
                                params.pop("title", None)
                                params.pop("additionalProperties", None)

                                props = params.get("properties")
                                if isinstance(props, dict):
                                    for prop_def in props.values():
                                        if isinstance(prop_def, dict):
                                            prop_def.pop("title", None)

                    cleaned_body = json.dumps(body_json).encode("utf-8")

                    # Rebuild request with cleaned content (and correct content-length)
                    request = httpx.Request(
                        method=original_request.method,
                        url=original_request.url,
                        headers=dict(original_request.headers),
                        content=cleaned_body,
                    )
                    request.headers["content-length"] = str(len(cleaned_body))
        except Exception:
            # If anything goes wrong, just send the original request
            request = original_request

        return await super().handle_async_request(request)


# Event hooks (kept, but do nothing)
async def log_request(_request: httpx.Request):
    return


async def log_response(_response: httpx.Response):
    return


# Create httpx client with custom transport and event hooks
httpx_client = httpx.AsyncClient(
    transport=SchemaCleaningTransport(),
    event_hooks={"request": [log_request], "response": [log_response]},
    timeout=60.0,
)

client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL, http_client=httpx_client)

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

###############################################################################
# All 13 tools (excluding place/cancel order for safety)
###############################################################################
tools: list[Tool] = [
    get_klines,
    get_ticker_price,
    get_best_ticker,
    get_order_book,
    search_crypto_news,
    search_global_news,
    get_account_info,
    get_crypto_holdings,
    get_crypto_orders,
    get_trading_pairs,
    get_best_price,
    get_recent_actions,
    log_action,
    log_tool_results,
]

crypto_trader_agent = Agent(
    name="DOGE_Analyzer",
    instructions="""You are DOGE_Analyzer, an autonomous Dogecoin trading analysis agent.

**MISSION**: Analyze DOGE market conditions every cycle and make a BUY, SELL, or HOLD decision.

**AUTONOMOUS WORKFLOW**:
1. Get Account Info: call get_account_info() to understand current holdings and buying power
2. Get DOGE price: call get_ticker_price(symbol="DOGEUSDT")
3. Get Trading Pairs: call get_trading_pairs(request={"from_currency":"DOGE", "to_currency":"USD"}) to see available DOGE pairs
4. Check order book: call get_order_book(request={"symbol":"DOGEUSDT","limit":int})
5. Get recent candles: call get_klines(symbol="DOGEUSDT", interval="15m", limit=int)
6. Search crypto news: call search_crypto_news(request={"search_string":"DOGE","limit":int})
7. Search global news: call search_global_news(request={"search_string":str,"articlesCount":int, "dateStart":"YYYY-MM-DD", "dateEnd":"YYYY-MM-DD", "apiKey":""})
8. Check holdings: call get_crypto_holdings()
9. Review recent actions: call get_recent_actions(limit=int)
10. MAKE DECISION: Based on ALL data, decide BUY, SELL, or HOLD
11. LOG DECISION: call log_action() with your decision
12. LOG TOOL RESULTS: call log_tool_results() with the analysis results
**DECISION CRITERIA**:
- BUY: Strong upward momentum, positive news, oversold conditions, order book shows demand
- SELL: Downward momentum, negative news, overbought conditions, order book shows supply pressure
- HOLD: Mixed signals, consolidation, waiting for clearer trend

**CRITICAL RULES**:
- ALWAYS use DOGEUSDT for Binance data
- ALWAYS use DOGE for Robinhood data
- Call tools sequentially, analyze results
- MUST make a decision every cycle (BUY/SELL/HOLD)
- MUST call log_action() with:
  * symbol: "DOGE"
  * side: "buy", "sell", or "hold"
  * quantity: float (for analysis, can be 0.0)
  * price: float (current DOGE price)
  * amount_usd: float (analysis only)
  * reason: str (detailed explanation of your decision)
  * profit_loss: float (analysis only)

**OUTPUT FORMAT**:
After analysis, state: "DECISION: [BUY/SELL/HOLD] - [Brief reason]"

Be systematic, data-driven, and always conclude with a logged decision.""",
    model=MODEL_NAME,
    tools=tools,
)

sql_lit_session = SQLiteSession(session_id="crypto_trader_v1", db_path="conversations.db")

###############################################################################


async def main():
    analysis_counter = 0
    ANALYSIS_INTERVAL = 900  # 15 minutes in seconds (change to 60 for testing)

    while True:
        try:
            analysis_counter += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"\nCycle #{analysis_counter} | {current_time}")

            autonomous_prompt = (
                "Analyze DOGE market conditions right now. "
                "Follow your workflow: get account info, get price, get trading pairs, check order book, analyze candles, search crypto news, search global news. "
                "check holdings, review recent actions, then make a BUY/SELL/HOLD decision and log it using log_action and log_tool_results."
            )

            result = Runner.run_streamed(
                starting_agent=crypto_trader_agent,
                input=autonomous_prompt,
                session=sql_lit_session,
            )

            final_output_chunks: list[str] = []

            async for event in result.stream_events():
                # Collect streaming text for final output
                if event.type == "raw_response_event" and isinstance(
                    event.data, ResponseTextDeltaEvent
                ):
                    final_output_chunks.append(event.data.delta)

                # Print ONLY the tool name (no URLs)
                elif event.type == "tool_call_event":
                    tool_name = event.data.get("name", "unknown_tool")
                    print(tool_name)

            # Print final agent output (full)
            final_text = "".join(final_output_chunks).strip()
            if final_text:
                print("\n" + final_text)

            next_time = datetime.fromtimestamp(time.time() + ANALYSIS_INTERVAL).strftime(
                "%H:%M:%S"
            )
            print(f"\nNext cycle at {next_time}")

            await asyncio.sleep(ANALYSIS_INTERVAL)

        except KeyboardInterrupt:
            print(f"\nStopped - Completed {analysis_counter} cycles")
            break
        except Exception as e:
            # Keep errors short, no noisy logs
            print(f"\nError: {str(e)[:200]}")
            await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"\nFatal error: {e}")
        raise
