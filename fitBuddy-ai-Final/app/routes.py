from .gemini_generator import generate_workout_gemini, generate_nutrition_gemini
from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .database import get_all_users

import os
import sqlite3
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@router.post("/generate")
async def generate(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    height: float = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    user_input = {
        "name": name,
        "age": age,
        "height": height,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
    }
    if os.getenv("DEMO_MODE", "false").lower() == "true":
        plan = (
            f"DEMO PLAN for {name} ({goal}, {intensity} intensity)\n\n"
            "Day 1: Warm-up 10 min, full-body strength 30 min\n"
            "Day 2: Cardio 30 min, core 10 min\n"
            "Day 3: Rest or light walk\n"
            "Day 4: Upper body strength 30 min\n"
            "Day 5: Lower body strength 30 min\n"
            "Day 6: HIIT 20 min, stretching\n"
            "Day 7: Rest"
        )
    else:
        try:
            workout = generate_workout_gemini(user_input)
            plan = f"WORKOUT PLAN\n\n{workout}"
        except Exception as e:
            print("GEMINI ERROR:", e)
            plan = f"Sorry, the AI could not respond right now. Please try again in a minute.\n\n{e}"

    return templates.TemplateResponse(request, "result.html", {"plan": plan, "name": name})  

@router.post("/feedback", response_class=HTMLResponse)
async def feedback(name: str = Form(""), rating: int = Form(...), comment: str = Form("")):
    conn = sqlite3.connect("fitbuddy.db")
    conn.execute("CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, rating INTEGER, comment TEXT)")
    conn.execute("INSERT INTO feedback (name, rating, comment) VALUES (?, ?, ?)", (name, rating, comment))
    conn.commit()
    conn.close()
    return HTMLResponse('<link rel="stylesheet" href="/static/style.css"><div class="card"><h1>Thank you!</h1><p class="sub">Your feedback was saved.</p><a class="btn" href="/">Home</a></div>')  