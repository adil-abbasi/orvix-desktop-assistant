from app.word_agent.active_word_reader import get_active_document_text
from app.word_agent.word_analyzer import analyze_text


def analyze_active_document(task):
    doc = get_active_document_text()

    if not doc["success"]:
        return {
            "success": False,
            "response": "No active document."
        }

    return analyze_text(
        doc["text"],
        task
    )