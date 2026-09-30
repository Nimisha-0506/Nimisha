"""Gemini Pro: workout and nutrition plan generator."""
from .ai_config import PRO_MODEL, ask_gemini


def generate_workout_gemini(user_input: dict) -> str:
    extra = ""
    if user_input.get("age"):
        extra += f"\nThe user is {user_input['age']} years old."
    if user_input.get("height"):
        extra += f" They are {user_input['height']} cm tall."
    if user_input.get("weight"):
        extra += f" They weigh {user_input['weight']} kg."
    prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of {user_input.get('goal', '')} at {user_input.get('intensity', '')} intensity.{extra}

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Days 2-7)

Use plain text, no markdown symbols.
"""
    return ask_gemini(prompt, PRO_MODEL)


def generate_nutrition_gemini(user_input: dict) -> str:
    prompt = f"""
You are a professional nutritionist.

Create a simple 7-day meal plan for a person with these details:
- Name: {user_input.get('name', '')}
- Age: {user_input.get('age', '')}
- Height: {user_input.get('height', '')} cm
- Weight: {user_input.get('weight', '')} kg
- Goal: {user_input.get('goal', '')}
- Activity level: {user_input.get('intensity', '')}

For each day give Breakfast, Lunch, Snack and Dinner.
Also give approximate daily calories, protein, carbs and fats,
plus 3 short hydration and eating tips.
Keep it practical, with easily available foods.
Use plain text, no markdown symbols.
"""
    return ask_gemini(PRO_MODEL, prompt)
