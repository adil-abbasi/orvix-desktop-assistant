from app.ai.gemini_provider import configure, ask_gemini, ask_gemini_stream
from app.ai.ollama_provider import ask_ollama
from app.ai.config.ai_config import AI_PROVIDER, GEMINI_API_KEY

try:
    from app.ai_cache import get_cached_response, set_cached_response
except Exception:
    get_cached_response = None
    set_cached_response = None


def configure_gemini_if_available():
    if GEMINI_API_KEY:
        configure(GEMINI_API_KEY)
    else:
        print("AI PROVIDER: Gemini API key missing. Gemini will be skipped or fallback will be used.")


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
        or "401" in error
        or "403" in error
        or "authentication" in error
        or "credentials" in error
        or "credential" in error
        or "api key" in error
        or "api_key" in error
        or "apikey" in error
        or "no api_key" in error
        or "adc" in error
        or "adc found" in error
        or "no api_key or adc found" in error
        or "access_token" in error
        or "permission" in error
        or "quota" in error
        or "rate limit" in error
        or "unsupported" in error
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


def ask_ai(prompt: str, use_cache=True):
    provider = str(AI_PROVIDER or "gemini").lower().strip()

    if use_cache and get_cached_response:
        try:
            cached = get_cached_response(prompt)
            if cached:
                return {
                    "success": True,
                    "response": cached,
                    "error": "",
                    "source": "cache"
                }
        except Exception:
            pass

    if provider == "ollama":
        print("AI PROVIDER: Using Ollama first...")

        ollama_result = ask_ollama(prompt)

        if ollama_result.get("success"):
            return ollama_result

        return {
            "success": False,
            "response": "",
            "error": ollama_result.get("error", "Ollama failed."),
            "source": "ollama"
        }

    print("AI PROVIDER: Trying Gemini...")

    gemini_result = {
        "success": False,
        "response": "",
        "error": "Gemini was not attempted.",
        "source": "gemini"
    }

    if GEMINI_API_KEY:
        try:
            configure_gemini_if_available()
            gemini_result = ask_gemini(prompt)
        except Exception as error:
            gemini_result = {
                "success": False,
                "response": "",
                "error": str(error),
                "source": "gemini"
            }
    else:
        gemini_result = {
            "success": False,
            "response": "",
            "error": "No GEMINI_API_KEY found.",
            "source": "gemini"
        }

    if gemini_result.get("success"):
        if use_cache and set_cached_response:
            try:
                set_cached_response(prompt, gemini_result.get("response", ""))
            except Exception:
                pass

        return gemini_result

    print("AI PROVIDER: Gemini failed.")
    print("AI PROVIDER GEMINI ERROR:", gemini_result.get("error", ""))

    print("AI PROVIDER: Trying Ollama fallback...")

    try:
        ollama_result = ask_ollama(prompt)
    except Exception as error:
        ollama_result = {
            "success": False,
            "response": "",
            "error": str(error),
            "source": "ollama"
        }

    if ollama_result.get("success"):
        if use_cache and set_cached_response:
            try:
                set_cached_response(prompt, ollama_result.get("response", ""))
            except Exception:
                pass

        return ollama_result

    print("AI PROVIDER: Ollama fallback failed.")
    print("AI PROVIDER OLLAMA ERROR:", ollama_result.get("error", ""))

    return {
        "success": False,
        "response": "",
        "error": (
            "Gemini failed: "
            + str(gemini_result.get("error", ""))
            + "\nOllama failed: "
            + str(ollama_result.get("error", ""))
        ),
        "source": "all_failed"
    }


def split_text_chunks(text: str, size: int = 80):
    text = str(text or "")

    for i in range(0, len(text), size):
        yield text[i:i + size]


def ask_ai_stream(prompt: str, provider=None):
    provider = str(provider or AI_PROVIDER or "gemini").lower().strip()

    if provider == "ollama":
        print("AI STREAM: Using Ollama non-streaming fallback.")

        try:
            result = ask_ollama(prompt)
        except Exception as error:
            result = {
                "success": False,
                "response": "",
                "error": str(error),
                "source": "ollama"
            }

        if result.get("success"):
            text = result.get("response", "")

            for chunk in split_text_chunks(text, 80):
                yield {
                    "success": True,
                    "text": chunk,
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

    print("AI STREAM: Trying Gemini streaming...")

    gemini_failed = False
    gemini_error = ""

    if GEMINI_API_KEY:
        try:
            configure_gemini_if_available()

            for chunk in ask_gemini_stream(prompt):
                if chunk.get("success") and chunk.get("text"):
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
    else:
        gemini_failed = True
        gemini_error = "No GEMINI_API_KEY found."

    if not gemini_failed:
        print("AI STREAM: Gemini streaming completed.")
        return

    print("AI STREAM: Gemini streaming failed.")
    print("AI STREAM GEMINI ERROR:", gemini_error)

    print("AI STREAM: Trying Ollama fallback...")

    try:
        fallback = ask_ollama(prompt)
    except Exception as fallback_error:
        fallback = {
            "success": False,
            "response": "",
            "error": str(fallback_error),
            "source": "ollama"
        }

    if fallback.get("success"):
        print("AI STREAM: Ollama fallback success.")

        text = fallback.get("response", "")

        for chunk in split_text_chunks(text, 80):
            yield {
                "success": True,
                "text": chunk,
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
        "source": "all_failed"
    }