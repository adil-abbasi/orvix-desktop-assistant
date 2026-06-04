import google.generativeai as genai

MODEL_NAME = "gemini-2.5-flash"


def configure(api_key):
    genai.configure(api_key=api_key)


def ask_gemini(prompt: str):
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        return {
            "success": True,
            "response": response.text,
            "error": ""
        }

    except Exception as e:
        return {
            "success": False,
            "response": "",
            "error": str(e)
        }