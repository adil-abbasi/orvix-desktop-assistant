from app.ai.gemini_provider import (
    configure,
    ask_gemini
)

from app.ai.ollama_provider import ask_ollama

from app.ai.config.ai_config import (
    GEMINI_API_KEY,
    AI_PROVIDER
)

configure(GEMINI_API_KEY)


def ask_ai(prompt: str, provider=None):
    provider = provider or AI_PROVIDER

    if provider == "gemini":
        return ask_gemini(prompt)

    if provider == "ollama":
        return ask_ollama(prompt)

    return {
        "success": False,
        "response": "",
        "error": "Unknown provider"
    }