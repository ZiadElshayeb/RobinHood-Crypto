from agents import (
    Agent,
    Runner,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    SQLiteSession,
    Tool
)
from openai.types.responses import ResponseTextDeltaEvent
from app.config import settings
from openai import AsyncOpenAI
import asyncio
import sys
import logging
import json
import httpx

# Import all tools (excluding place and cancel order for safety)
from app.agents.tools.binance_market_data import get_klines, get_ticker_price
from app.agents.tools.binance_order_book import get_best_ticker, get_order_book
from app.agents.tools.crypto_news import search_crypto_news
from app.agents.tools.global_news import search_global_news
from app.agents.tools.robinhood_account import (
    get_account_info,
    get_crypto_holdings,
    get_crypto_orders,
    get_trading_pairs
)
from app.agents.tools.robinhood_prices import get_best_price
from app.agents.tools.actions_history import get_recent_actions, log_action
from datetime import datetime
import time

# Fix for Windows async compatibility
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Configure logging: DEBUG to file, INFO to console
file_handler = logging.FileHandler('agent_debug.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Only INFO and above to console
console_handler.setFormatter(logging.Formatter('%(message)s'))  # Clean format without timestamps

logging.basicConfig(
    level=logging.DEBUG,  # Capture everything
    handlers=[file_handler, console_handler]
)

# Library logging: DEBUG to file only, WARNING to console
logging.getLogger("httpx").setLevel(logging.DEBUG)
logging.getLogger("openai").setLevel(logging.DEBUG)
logging.getLogger("httpx").handlers = [file_handler]
logging.getLogger("openai").handlers = [file_handler]

logger = logging.getLogger(__name__)

BASE_URL = settings.GEMINI_BASE_URL
API_KEY = settings.GEMINI_API_KEY
MODEL_NAME = settings.GEMINI_MODEL

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set BASE_URL, API_KEY, MODEL_NAME via .env"
    )

###############################################################################

# Custom httpx Transport that modifies requests before sending
class SchemaCleaningTransport(httpx.AsyncHTTPTransport):
    async def handle_async_request(self, request):
        # Clean tool schemas before sending
        original_request = request
        cleaned_count = 0
        
        try:
            if request.content and b'tools' in request.content:
                body = request.content.decode('utf-8')
                body_json = json.loads(body)
                
                if 'tools' in body_json:
                    # Clean tool schemas (remove Gemini-incompatible fields)
                    for idx, tool in enumerate(body_json['tools']):
                        if 'function' in tool:
                            func = tool['function']
                            tool_name = func.get('name', 'unknown')
                            had_strict = 'strict' in func
                            
                            # Remove Gemini-incompatible fields
                            func.pop('strict', None)
                            
                            if 'parameters' in func:
                                params = func['parameters']
                                params.pop('title', None)
                                params.pop('additionalProperties', None)
                                
                                if 'properties' in params:
                                    for prop_def in params['properties'].values():
                                        prop_def.pop('title', None)
                            
                            if had_strict:
                                cleaned_count += 1
                            
                            # Detailed per-tool logging to DEBUG (file only)
                            logger.debug(f"  Tool {idx+1}: {tool_name} (strict removed: {had_strict})")
                    
                    # Re-encode with cleaned schemas
                    cleaned_body = json.dumps(body_json).encode('utf-8')
                    
                    # Create new request with cleaned content and updated headers
                    request = httpx.Request(
                        method=original_request.method,
                        url=original_request.url,
                        headers=dict(original_request.headers),
                        content=cleaned_body
                    )
                    request.headers['content-length'] = str(len(cleaned_body))
                    
                    # Summary to console (INFO level)
                    logger.info(f"  → Schema cleaned: {cleaned_count} tools prepared for Gemini API")
                    logger.debug(f"[TRANSPORT] Body size: {len(cleaned_body)} bytes (was {len(original_request.content)} bytes)")
        except Exception as e:
            logger.error(f"Error cleaning request: {e}", exc_info=True)
        
        # Continue with the (possibly cleaned) request
        return await super().handle_async_request(request)

# Event hooks - minimal logging (file only via DEBUG)
async def log_request(request):
    # Log to file only (DEBUG level filtered from console)
    logger.debug(f"[REQUEST] {request.method} {request.url}")
    try:
        if request.content and b'tools' in request.content:
            body_json = json.loads(request.content.decode('utf-8'))
            if 'tools' in body_json:
                logger.debug(f"  Tools: {len(body_json['tools'])} defined")
            if 'messages' in body_json:
                logger.debug(f"  Messages: {len(body_json['messages'])} in conversation")
    except:
        pass

async def log_response(response):
    # Log to file only (DEBUG level filtered from console)
    logger.debug(f"[RESPONSE] Status: {response.status_code}")

# Create httpx client with custom transport and event hooks
httpx_client = httpx.AsyncClient(
    transport=SchemaCleaningTransport(),
    event_hooks={
        'request': [log_request],
        'response': [log_response]
    },
    timeout=60.0
)

client = AsyncOpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
            http_client=httpx_client
        )

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

###############################################################################

# All 13 tools (excluding place/cancel order for safety)
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
]

# Note: Tool schema cleaning (removing 'strict', 'title', etc.) happens in log_request()
# before the request is sent to Gemini, ensuring clean schemas every time

crypto_trader_agent = Agent(
    name="DOGE_Analyzer",
    instructions="""You are DOGE_Analyzer, an autonomous Dogecoin trading analysis agent.

**MISSION**: Analyze DOGE market conditions every cycle and make a BUY, SELL, or HOLD decision.

**AUTONOMOUS WORKFLOW**:
1. Get DOGE price: call get_ticker_price(symbol="DOGEUSDT")
2. Check order book: call get_order_book(request={"symbol":"DOGEUSDT","limit":20})
3. Get recent candles: call get_klines(symbol="DOGEUSDT", interval="15m", limit=96)
4. Search news: call search_crypto_news(request={"search_string":"DOGE","limit":5})
5. Check holdings: call get_crypto_holdings()
6. Review recent actions: call get_recent_actions(limit=5)
7. MAKE DECISION: Based on ALL data, decide BUY, SELL, or HOLD
8. LOG DECISION: call log_action() with your decision

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
  * quantity: 0.0 (analysis only)
  * price: current DOGE price
  * amount_usd: 0.0 (analysis only)
  * reason: detailed explanation of your decision
  * profit_loss: 0.0 (analysis only)

**OUTPUT FORMAT**:
After analysis, state: "DECISION: [BUY/SELL/HOLD] - [Brief reason]"

Be systematic, data-driven, and always conclude with a logged decision.""",
    model=MODEL_NAME,
    tools=tools
)

sql_lit_session = SQLiteSession(session_id="crypto_trader_v1", db_path='conversations.db')

###############################################################################

async def main():
    print("="*80)
    print("🐕 DOGE AUTONOMOUS ANALYZER - PRODUCTION MODE")
    print("="*80)
    print("\n[i] Target: Dogecoin (DOGE) - Autonomous Decision Making")
    print("[i] Available Tools: 13 tools loaded")
    print("    - Market Data: get_klines, get_ticker_price, get_best_ticker, get_order_book")
    print("    - News: search_crypto_news, search_global_news")
    print("    - Account: get_account_info, get_crypto_holdings, get_crypto_orders, get_trading_pairs")
    print("    - Prices: get_best_price")
    print("    - History: get_recent_actions, log_action")
    print("\n[!] ANALYSIS MODE - Decisions logged, no actual trades executed")
    print("[i] Analysis interval: Every 15 minutes")
    print("\n[DEBUG] Comprehensive logging enabled - check agent_debug.log")
    print("\nPress Ctrl+C to stop the autonomous analyzer")
    print("="*80)
    
    analysis_counter = 0
    ANALYSIS_INTERVAL = 900  # 15 minutes in seconds (change to 60 for testing)
    
    while True:
        try:
            analysis_counter += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            logger.debug(f"\n{'='*80}\nSTARTING ANALYSIS CYCLE #{analysis_counter}\n{'='*80}")
            
            print(f"\n\n{'='*80}")
            print(f"🐕 DOGE Analysis Cycle #{analysis_counter}")
            print(f"⏰ Time: {current_time}")
            print("="*80)
            
            # Log the tools being passed
            logger.debug(f"Tools being passed to agent: {[t.name if hasattr(t, 'name') else str(t) for t in tools]}")
            
            # Autonomous prompt - agent analyzes DOGE and makes decision
            autonomous_prompt = (
                "Analyze DOGE market conditions right now. "
                "Follow your workflow: get price, check order book, analyze candles, search news, "
                "check holdings, review recent actions, then make a BUY/SELL/HOLD decision and log it using log_action."
            )
            
            result = Runner.run_streamed(
                starting_agent=crypto_trader_agent,
                input=autonomous_prompt,
                session=sql_lit_session,
            )
            
            print("\n[AI] CryptoTrader: ", end="", flush=True)
            
            # Track tool usage and stream state
            tools_used = []
            api_call_count = 0
            seen_event_ids = set()  # Track processed events to prevent duplicates
            
            async for event in result.stream_events():
                # Log every event type for debugging
                event_data = getattr(event, 'data', None)
                logger.debug(f"Event type: {event.type}, Data: {str(event_data)[:200] if event_data else 'N/A'}")
                
                # Generate event ID to prevent duplicate processing
                event_id = f"{event.type}_{id(event)}_{getattr(event_data, 'delta', '')}"
                
                # Print ONLY streaming text deltas (incremental updates)
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    if event_id not in seen_event_ids:
                        print(event.data.delta, end="", flush=True)
                        seen_event_ids.add(event_id)
                
                # Track and display tool calls
                elif event.type == "tool_call_event":
                    api_call_count += 1
                    tool_name = event.data.get("name", "unknown_tool")
                    tool_args = event.data.get("arguments", {})
                    tools_used.append(tool_name)
                    logger.debug(f"\n[TOOL CALL #{api_call_count}] {tool_name}")
                    logger.debug(f"Arguments: {json.dumps(tool_args, indent=2)}")
                    print(f"\n  → Calling tool: {tool_name}")
                
                # Log tool results (details in debug log only)
                elif event.type == "tool_result_event":
                    tool_name = event.data.get("name", "unknown_tool")
                    tool_result = event.data.get("result", "")
                    logger.debug(f"Tool result for {tool_name}: {str(tool_result)[:500]}")
                    print(f"  ✓ Tool {tool_name} completed")
                
                # Skip duplicate message events (already printed via streaming)
                elif event.type in ["message_event", "output_event"]:
                    pass  # Already handled via streaming text deltas
            
            print()  # New line after streaming completes
            
            # Summary
            if tools_used:
                print("\n" + "="*80)
                print(f"📊 Summary: {len(set(tools_used))} unique tools used ({len(tools_used)} total calls): {', '.join(set(tools_used))}")
                # Check if decision was logged
                if 'log_action' in tools_used:
                    print("✅ Decision logged to database")
                else:
                    print("⚠️  WARNING: No decision logged this cycle")
                
                print("="*80)
            
            logger.debug(f"\n{'='*80}\nCOMPLETED ANALYSIS CYCLE #{analysis_counter}\n{'='*80}\n")
            
            # Wait for next analysis cycle
            print(f"\n⏳ Waiting {ANALYSIS_INTERVAL//60} minutes until next analysis...")
            print(f"   Next cycle at: {datetime.fromtimestamp(time.time() + ANALYSIS_INTERVAL).strftime('%Y-%m-%d %H:%M:%S')}")
            
            await asyncio.sleep(ANALYSIS_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n[STOP] Autonomous analyzer stopped by user")
            print(f"[INFO] Completed {analysis_counter} analysis cycles")
            break
        except Exception as e:
            logger.error(f"Error in analysis cycle #{analysis_counter}: {e}", exc_info=True)
            print(f"\n❌ Error in analysis cycle: {e}")
            print(f"   Retrying in 60 seconds...")
            await asyncio.sleep(60)  # Wait 1 minute before retry

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[BYE] Session interrupted. Goodbye!")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        raise
