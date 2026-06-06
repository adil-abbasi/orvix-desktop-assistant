from app.word_agent.active_word_reader import get_active_document_text
from app.word_agent.word_analyzer import analyze_text
from app.word_agent.word_live_agent import live_insert_text


def execute_document_action(user_command):
    doc = get_active_document_text()

    if not doc.get("success"):
        return {
            "success": False,
            "message": "No active Word document found."
        }

    document_text = doc.get("text", "")

    prompt = f"""
You are Orvix Document Assistant.

Current document:
{document_text}

User request:
{user_command}

Rules:
- Perform exactly what the user requested.
- Return only the content to insert.
- Do not explain what you are doing.
- Do not repeat existing content unless required.
"""

    result = analyze_text(
        document_text,
        prompt
    )

    if not result.get("success"):
        return {
            "success": False,
            "message": result.get("error", "AI failed")
        }

    live_insert_text(
        "\n\n" + result["response"],
        delay=0.05
    )

    return {
        "success": True,
        "message": "Document updated."
    }