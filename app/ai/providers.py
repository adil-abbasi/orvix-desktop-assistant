from app.ai.gemini_provider import configure, ask_gemini, ask_gemini_stream
from app.ai.ollama_provider import ask_ollama
from app.ai.config.ai_config import AI_PROVIDER, GEMINI_API_KEY
from app.ai_cache import get_cached_response, set_cached_response


configure(GEMINI_API_KEY)


def is_quota_error(error: str):
    error = error.lower()

    return (
        "429" in error
        or "quota" in error
        or "too many requests" in error
        or "rate limit" in error
    )


def ask_ai(prompt: str, provider=None, use_cache=True):
    provider = provider or AI_PROVIDER

    if use_cache:
        cached = get_cached_response(prompt)

        if cached:
            return cached

    if provider == "gemini":
        result = ask_gemini(prompt)

        if result.get("success"):
            if use_cache:
                set_cached_response(prompt, result)

            return result

        if is_quota_error(result.get("error", "")):
            fallback = ask_ollama(prompt)

            if fallback.get("success") and use_cache:
                set_cached_response(prompt, fallback)

            return fallback

        return result

    if provider == "ollama":
        result = ask_ollama(prompt)

        if result.get("success") and use_cache:
            set_cached_response(prompt, result)

        return result

    return {
        "success": False,
        "response": "",
        "error": f"Unknown provider: {provider}"
    }


def ask_ai_stream(prompt: str, provider=None):
    """
    Streaming AI response for live writing.
    For now, streaming is supported only for Gemini.
    """

    provider = provider or AI_PROVIDER

    if provider == "gemini":
        yield from ask_gemini_stream(prompt)
        return

    # Ollama streaming can be added later.
    # For now, return a clean error instead of crashing.
    yield {
        "success": False,
        "text": "",
        "error": f"Streaming is not supported for provider: {provider}"
    }