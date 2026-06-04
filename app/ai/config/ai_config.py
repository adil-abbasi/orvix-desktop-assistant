
import os
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "gemini")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AQ.Ab8RN6IvpspFKioYyxE-n2suQ3UCDFz4hjk8mArzkWP0nPtLKg")