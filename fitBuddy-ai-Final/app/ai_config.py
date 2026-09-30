"""Shared Gemini configuration + helper used by all AI modules."""
import os
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

API_KEY = os.getenv("GOOGLE_API_KEY")
PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-3.8-flash")
FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.8-flash")

if API_KEY:
    genai.configure(api_key=API_KEY)


def ask_gemini(model_name: str, prompt: str) -> str:
    """Send a prompt to Gemini and return clean text. Raises RuntimeError on failure."""
    if not API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is not set. Add it to the .env file and restart the server.")
    try:
        response = genai.GenerativeModel(model_name).generate_content(prompt)
        text = (response.text or "").strip()
    except Exception as e:  # blocked content, quota, network, bad model name...
        raise RuntimeError(f"Gemini request failed ({model_name}): {e}") from e
    if not text:
        raise RuntimeError("Gemini returned an empty response. Please try again.")
    return text