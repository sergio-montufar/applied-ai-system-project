import os
from typing import Literal

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()


class Hint(BaseModel):
    direction: Literal["higher", "lower", "correct"]
    message: str


SYSTEM_PROMPT = """You are a friendly hint coach for a number-guessing game.

Given a player's guess and the secret number, return:
- direction: "higher" if the secret is greater than the guess, "lower" if the secret is less than the guess, "correct" if they are equal
- message: a short, playful natural-language hint (under 15 words) that nudges the player toward the secret

Rules:
- NEVER reveal the secret number. Do not include the secret as a digit anywhere in the message.
- Use magnitude words like "way", "much", "a bit", "very close" based on how far the guess is from the secret.
- Keep the tone encouraging."""


_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        _client = genai.Client()
    return _client


def generate_hint(guess: int, secret: int, attempts_left: int) -> Hint:
    """Ask Gemini to produce a structured hint for the given guess vs. secret."""
    client = _get_client()
    user_msg = (
        f"Player's guess: {guess}\n"
        f"Secret number: {secret}\n"
        f"Attempts left: {attempts_left}\n"
        "Generate a hint."
    )
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview",
        contents=user_msg,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=Hint,
        ),
    )
    if response.parsed is None:
        raise RuntimeError("Gemini did not return a parsable Hint object")
    return response.parsed
