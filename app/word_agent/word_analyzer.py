from app.ai.providers import ask_ai


def analyze_text(text, task):
    prompt = f"""
You are Orvix document assistant.

Task:
{task}

Document text:
{text}

Return a clear, useful response.
"""

    result = ask_ai(prompt)

    if result.get("success"):
        return {
            "success": True,
            "response": result.get("response", "")
        }

    return {
        "success": False,
        "response": "",
        "error": result.get("error", "AI failed")
    }