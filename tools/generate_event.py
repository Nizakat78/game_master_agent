from agents import function_tool, RunContextWrapper, AsyncOpenAI
from typing import TypedDict
import os
from dotenv import load_dotenv, find_dotenv
from set_config import model

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

class GenerateEventInput(TypedDict):
    situation: str

class GenerateEventOutput(TypedDict):
    event: str

@function_tool
async def generate_event(wrapper: RunContextWrapper, input: GenerateEventInput) -> GenerateEventOutput:
    """
    Generates a short immersive game event based on the situation.
    """
    situation = (input.get("situation") or "The player finds themselves in a mysterious place.").strip()

    prompt = (
        f"[TOOL: generate_event] You are a fantasy game event generator.\n"
        f"Situation: {situation}\n"
        "Generate a short immersive event (2–3 sentences)."
    )

    response = await client.chat.completions.create(
        model=getattr(model, "model_id", "gemini-2.5-flash"),
        messages=[{"role": "user", "content": prompt}],
    )

    content = (
        getattr(response.choices[0].message, "content", None)
        or getattr(response.choices[0], "text", None)
        or ""
    )

    return {"event": content.strip()}
