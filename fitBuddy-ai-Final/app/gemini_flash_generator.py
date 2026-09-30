"""Gemini Flash: quick nutrition / recovery tips."""
from .ai_config import FLASH_MODEL, ask_gemini


def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = (
        f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand (2-3 sentences)."
    )
    return ask_gemini(FLASH_MODEL, prompt)