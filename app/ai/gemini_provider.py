from google import genai

MODEL_NAME = "gemini-2.5-flash"

_client = None


def configure(api_key):
    global _client

    _client = genai.Client(
        api_key=api_key
    )


def extract_response_text(response):
    try:
        if response.text:
            return response.text
    except Exception:
        pass

    return ""


def ask_gemini(prompt: str):
    try:
        if _client is None:
            return {
                "success": False,
                "response": "",
                "error": "Gemini client is not configured."
            }

        response = _client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        text = extract_response_text(response)

        if not text:
            return {
                "success": False,
                "response": "",
                "error": "Gemini returned empty response."
            }

        return {
            "success": True,
            "response": text,
            "error": ""
        }

    except Exception as e:
        return {
            "success": False,
            "response": "",
            "error": str(e)
        }