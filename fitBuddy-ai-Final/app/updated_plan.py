"""Gemini Pro: revise an existing plan using user feedback."""
from .ai_config import PRO_MODEL, ask_gemini


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    prompt = f"""
You are a professional fitness trainer assistant.

Here's the original 7-day workout plan:
{original_plan}

User Feedback:
"{user_feedback}"

Based on the feedback, revise the relevant parts of the workout plan. Keep the format and the rest of the plan unchanged if not needed. Return the full updated 7-day plan.
"""
    return ask_gemini(PRO_MODEL, prompt)