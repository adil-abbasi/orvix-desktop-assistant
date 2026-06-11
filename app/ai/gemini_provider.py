import google.generativeai as genai

MODEL_NAME = "gemini-2.5-pro"


def configure(api_key):
    try:
        genai.configure(api_key=api_key)
        print("GEMINI: API configured.")
    except Exception as error:
        print("GEMINI: Failed to configure API.")
        print("GEMINI CONFIG ERROR:", error)


def extract_response_text(response):
    try:
        if hasattr(response, "text") and response.text:
            return response.text.strip()
    except Exception:
        pass

    try:
        parts = []

        for candidate in response.candidates:
            content = candidate.content

            for part in content.parts:
                if hasattr(part, "text") and part.text:
                    parts.append(part.text)

        return "\n".join(parts).strip()

    except Exception:
        return ""


def clean_gemini_error(error):
    error_text = str(error)

    if "429" in error_text or "quota" in error_text.lower():
        return f"Gemini quota/rate limit error: {error_text}"

    if "timeout" in error_text.lower():
        return f"Gemini timeout error: {error_text}"

    if "api key" in error_text.lower():
        return f"Gemini API key error: {error_text}"

    return error_text


def ask_gemini(prompt: str):
    try:
        print(f"GEMINI: Trying model {MODEL_NAME}...")

        model = genai.GenerativeModel(MODEL_NAME)

        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 1200,
        }

        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            request_options={
                "timeout": 35
            }
        )

        text = extract_response_text(response)

        if not text:
            return {
                "success": False,
                "response": "",
                "error": "Gemini returned empty response.",
                "source": "gemini"
            }

        print("GEMINI: Response generated successfully.")

        return {
            "success": True,
            "response": text,
            "error": "",
            "source": "gemini"
        }

    except Exception as error:
        clean_error = clean_gemini_error(error)

        print("GEMINI: Failed.")
        print("GEMINI ERROR:", clean_error)

        return {
            "success": False,
            "response": "",
            "error": clean_error,
            "source": "gemini"
        }


def ask_gemini_stream(prompt: str):
    """
    Streams Gemini response chunk by chunk.
    This allows Orvix to write into Word while AI is still generating.
    """

    try:
        print(f"GEMINI STREAM: Trying model {MODEL_NAME}...")

        model = genai.GenerativeModel(MODEL_NAME)

        generation_config = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 2500,
        }

        response_stream = model.generate_content(
            prompt,
            generation_config=generation_config,
            stream=True,
            request_options={
                "timeout": 60
            }
        )

        has_output = False

        for chunk in response_stream:
            text = extract_response_text(chunk)

            if text:
                has_output = True

                yield {
                    "success": True,
                    "text": text,
                    "error": "",
                    "source": "gemini_stream"
                }

        if not has_output:
            yield {
                "success": False,
                "text": "",
                "error": "Gemini stream returned empty response.",
                "source": "gemini_stream"
            }

        print("GEMINI STREAM: Completed.")

    except Exception as error:
        clean_error = clean_gemini_error(error)

        print("GEMINI STREAM: Failed.")
        print("GEMINI STREAM ERROR:", clean_error)

        yield {
            "success": False,
            "text": "",
            "error": clean_error,
            "source": "gemini_stream"
        }