from agents import (
    Agent,
    Runner,
    function_tool,
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
from app.agents.tools.crypto_news import search_crypto_news

BASE_URL = settings.GEMINI_BASE_URL
API_KEY = settings.GEMINI_API_KEY
MODEL_NAME = settings.GEMINI_MODEL

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set BASE_URL, API_KEY, MODEL_NAME via .env"
    )

###############################################################################

client = AsyncOpenAI(
            api_key=API_KEY,
            base_url=BASE_URL
        )

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

###############################################################################

tools: list[Tool] = [search_crypto_news]

test_agent = Agent(
        name= "Mark",
        instructions="you are a helpful assistance named 'mark', use your tools to help you answering user queries accurately.",
        model=MODEL_NAME,
        tools=tools
    )

sql_lit_session = SQLiteSession(session_id="2", db_path='conversations.db')

###############################################################################

async def main():
    print("Chat with Mark (type 'exit' or 'quit' to end)")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        result = Runner.run_streamed(starting_agent=test_agent,
                                    input=user_input,
                                    session=sql_lit_session,
                                )
        
        print(f"\nMark: ", end="", flush=True)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                print(event.data.delta, end="", flush=True)
        print()  # New line after streaming completes

if __name__ == "__main__":
    asyncio.run(main())
