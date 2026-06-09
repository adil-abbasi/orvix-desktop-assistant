from app.ai.gemini_provider import configure, ask_gemini, ask_gemini_stream
from app.ai.ollama_provider import ask_ollama
from app.ai.config.ai_config import AI_PROVIDER, GEMINI_API_KEY
from app.ai_cache import get_cached_response, set_cached_response


configure(GEMINI_API_KEY)


def is_quota_error(error: str):
    error = str(error or "").lower()

    return (
        "429" in error
        or "quota" in error
        or "too many requests" in error
        or "rate limit" in error
        or "resource_exhausted" in error
        or "exceeded" in error
    )


def is_provider_error(error: str):
    error = str(error or "").lower()

    return (
        is_quota_error(error)
        or "timeout" in error
        or "connection" in error
        or "network" in error
        or "unavailable" in error
        or "failed" in error
    )


def mark_source(result: dict, source: str):
    if not isinstance(result, dict):
        return {
            "success": False,
            "response": "",
            "error": "Invalid provider result.",
            "source": source
        }

    result["source"] = source
    return result


def ask_ai(prompt: str, provider=None, use_cache=True):
    provider = provider or AI_PROVIDER

    if use_cache:
        cached = get_cached_response(prompt)

        if cached:
            cached["source"] = cached.get("source", "cache")
            print("AI PROVIDER: Using cached response.")
            return cached

    if provider == "gemini":
        print("AI PROVIDER: Trying Gemini...")

        try:
            result = ask_gemini(prompt)
        except Exception as error:
            result = {
                "success": False,
                "response": "",
                "error": str(error)
            }

        result = mark_source(result, "gemini")

        if result.get("success"):
            print("AI PROVIDER: Gemini success.")

            if use_cache:
                set_cached_response(prompt, result)

            return result

        error = result.get("error", "")
        print("AI PROVIDER: Gemini failed.")
        print("AI PROVIDER GEMINI ERROR:", error)

        if is_provider_error(error):
            print("AI PROVIDER: Trying Ollama fallback...")

            try:
                fallback = ask_ollama(prompt)
            except Exception as fallback_error:
                fallback = {
                    "success": False,
                    "response": "",
                    "error": str(fallback_error)
                }

            fallback = mark_source(fallback, "ollama")

            if fallback.get("success"):
                print("AI PROVIDER: Ollama fallback success.")

                if use_cache:
                    set_cached_response(prompt, fallback)

                return fallback

            print("AI PROVIDER: Ollama fallback failed.")
            print("AI PROVIDER OLLAMA ERROR:", fallback.get("error", ""))

            return {
                "success": False,
                "response": "",
                "error": (
                    "Gemini failed and Ollama fallback also failed. "
                    f"Gemini error: {error}. "
                    f"Ollama error: {fallback.get('error', '')}"
                ),
                "source": "none"
            }

        return result

    if provider == "ollama":
        print("AI PROVIDER: Trying Ollama...")

        try:
            result = ask_ollama(prompt)
        except Exception as error:
            result = {
                "success": False,
                "response": "",
                "error": str(error)
            }

        result = mark_source(result, "ollama")

        if result.get("success"):
            print("AI PROVIDER: Ollama success.")

            if use_cache:
                set_cached_response(prompt, result)

        else:
            print("AI PROVIDER: Ollama failed.")
            print("AI PROVIDER OLLAMA ERROR:", result.get("error", ""))

        return result

    return {
        "success": False,
        "response": "",
        "error": f"Unknown provider: {provider}",
        "source": "none"
    }


def ask_ai_stream(prompt: str, provider=None):
    """
    Streaming AI response for live writing.

    Flow:
    - Gemini supports real streaming.
    - If Gemini fails/quota, try Ollama non-streaming and split response into chunks.
    - If Ollama also fails, return clean error.
    """

    provider = provider or AI_PROVIDER

    if provider == "gemini":
        print("AI STREAM: Trying Gemini streaming...")

        gemini_failed = False
        gemini_error = ""

        try:
            for chunk in ask_gemini_stream(prompt):
                if chunk.get("success"):
                    yield {
                        "success": True,
                        "text": chunk.get("text", ""),
                        "error": "",
                        "source": "gemini_stream"
                    }
                else:
                    gemini_failed = True
                    gemini_error = chunk.get("error", "Gemini streaming failed.")
                    break

        except Exception as error:
            gemini_failed = True
            gemini_error = str(error)

        if not gemini_failed:
            print("AI STREAM: Gemini streaming completed.")
            return

        print("AI STREAM: Gemini streaming failed.")
        print("AI STREAM GEMINI ERROR:", gemini_error)

        if is_provider_error(gemini_error):
            print("AI STREAM: Trying Ollama fallback...")

            try:
                fallback = ask_ollama(prompt)
            except Exception as fallback_error:
                fallback = {
                    "success": False,
                    "response": "",
                    "error": str(fallback_error)
                }

            if fallback.get("success"):
                print("AI STREAM: Ollama fallback success.")

                text = fallback.get("response", "")

                for i in range(0, len(text), 80):
                    yield {
                        "success": True,
                        "text": text[i:i + 80],
                        "error": "",
                        "source": "ollama_fallback"
                    }

                return

            print("AI STREAM: Ollama fallback failed.")
            print("AI STREAM OLLAMA ERROR:", fallback.get("error", ""))

            yield {
                "success": False,
                "text": "",
                "error": (
                    "Gemini streaming failed and Ollama fallback also failed. "
                    f"Gemini error: {gemini_error}. "
                    f"Ollama error: {fallback.get('error', '')}"
                ),
                "source": "none"
            }
            return

        yield {
            "success": False,
            "text": "",
            "error": gemini_error,
            "source": "gemini_stream"
        }
        return

    if provider == "ollama":
        print("AI STREAM: Using Ollama non-streaming fallback.")

        try:
            result = ask_ollama(prompt)
        except Exception as error:
            result = {
                "success": False,
                "response": "",
                "error": str(error)
            }

        if result.get("success"):
            text = result.get("response", "")

            for i in range(0, len(text), 80):
                yield {
                    "success": True,
                    "text": text[i:i + 80],
                    "error": "",
                    "source": "ollama"
                }

            return

        yield {
            "success": False,
            "text": "",
            "error": result.get("error", "Ollama failed."),
            "source": "ollama"
        }
        return

    yield {
        "success": False,
        "text": "",
        "error": f"Streaming is not supported for provider: {provider}",
        "source": "none"
    }