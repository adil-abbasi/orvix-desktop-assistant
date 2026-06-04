from app.ai.gemini_provider import configure, ask_gemini
from app.ai.config.ai_config import GEMINI_API_KEY

configure(GEMINI_API_KEY)

result = ask_gemini("Say hello from Orvix.")
print(result)