import os
from agent.agent import Agent
from .prompts import INSTRUCTIONS

agent = Agent(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=f"http://127.0.0.1:{os.getenv('PORT', '8000')}",
    model_name=os.getenv("GEMINI_MODEL_DEV", "gemini-2.5-flash-lite"),
    temperature=os.getenv("TEMPERATURE_DEV", 0.2),
    instructions=INSTRUCTIONS,
    tools_prefix="/infra",
)
