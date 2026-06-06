import google.generativeai as genai

MODEL_NAME = "gemini-2.5-flash"


def configure(api_key):
    genai.configure(api_key=api_key)


def extract_response_text(response):
    try:
        if hasattr(response, "text") and response.text:
            return response.text
    except Exception:
        pass

    try:
        parts = []

        for candidate in response.candidates:
            content = candidate.content

            for part in content.parts:
                if hasattr(part, "text"):
                    parts.append(part.text)

        return "\n".join(parts)

    except Exception:
        return ""


def ask_gemini(prompt: str):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

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