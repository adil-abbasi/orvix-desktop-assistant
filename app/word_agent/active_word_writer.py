from app.word_agent.active_word_reader import get_active_document_text
from app.word_agent.word_analyzer import analyze_text
from app.word_agent.word_live_agent import live_insert_text


def continue_active_document(user_command):
    doc = get_active_document_text()

    if not doc.get("success"):
        return {
            "success": False,
            "message": "No active Word document found."
        }

    current_text = doc.get("text", "")

    task = f"""
Continue this document based on the user's instruction.

User instruction:
{user_command}

Current document:
{current_text}

Rules:
- Do not repeat existing content.
- Add useful new sections.
- Keep writing style professional.
- Return only the new content to append.
"""

    result = analyze_text(
        current_text,
        task
    )

    if not result.get("success"):
        return {
            "success": False,
            "message": result.get("error", "AI failed.")
        }

    live_insert_text(
        "\n\n" + result["response"],
        delay=0.05
    )

    return {
        "success": True,
        "message": "Continued writing in active Word document."
    }