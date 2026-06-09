import os
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini").lower().strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()


if AI_PROVIDER == "gemini" and not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY is missing. Gemini will not work.")