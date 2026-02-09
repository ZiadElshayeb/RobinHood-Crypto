from agents import (
    Agent,
    Runner,
    function_tool,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
from agents.extensions.models.litellm_model import LitellmModel
from app.config import settings
from openai import AsyncOpenAI
import asyncio

BASE_URL = settings.GEMINI_BASE_URL
API_KEY = settings.GEMINI_API_KEY
MODEL_NAME = settings.GEMINI_MODEL

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set BASE_URL, API_KEY, MODEL_NAME via .env"
    )

client = AsyncOpenAI(
            api_key=API_KEY,
            base_url=BASE_URL
        )

set_default_openai_client(client=client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(disabled=True)

async def main():
    basic_agent = Agent(
        name= "Basic Agent",
        instructions="response with hello world to agents",
        model=MODEL_NAME
    )

    response = await Runner.run(starting_agent=basic_agent, input="hello")
    print(response.final_output)

if __name__ == "__main__":
    asyncio.run(main())
