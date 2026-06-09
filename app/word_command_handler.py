import re

from app.word_agent.word_memory import load_current_document
from app.word_agent.word_reader import read_word_document
from app.word_agent.word_analyzer import analyze_text
from app.word_agent.word_writer import append_to_word_document


def detect_word_name(text, default_name="OrvixDocument"):
    match = re.search(r"named\s+([A-Za-z0-9_\-]+)", text, re.IGNORECASE)
    if match:
        return match.group(1)

    match = re.search(r"name\s+([A-Za-z0-9_\-]+)", text, re.IGNORECASE)
    if match:
        return match.group(1)

    match = re.search(r"called\s+([A-Za-z0-9_\-]+)", text, re.IGNORECASE)
    if match:
        return match.group(1)

    return default_name


def extract_topic(text):
    match = re.search(r"about\s+(.+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    match = re.search(r"on\s+(.+)", text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    return text.strip()


def detect_document_type(text):
    text = text.lower()

    if "assignment" in text:
        return "assignment"

    if "research" in text or "research paper" in text:
        return "research report"

    if "essay" in text:
        return "essay"

    if "proposal" in text:
        return "proposal"

    if "notes" in text or "study notes" in text:
        return "study notes"

    if "summary" in text or "summarize" in text:
        return "summary"

    if "letter" in text:
        return "letter"

    if "application" in text:
        return "application"

    return "document"


def is_word_creation_command(user_command: str):
    text = user_command.lower()

    return (
        ("create" in text or "make" in text or "generate" in text)
        and (
            "word" in text
            or "docx" in text
            or "ms word" in text
            or "word file" in text
            or "word document" in text
        )
    )


def build_word_creation_plan(user_command: str):
    """
    This function only creates a plan.
    It does not open Word.
    It does not generate AI content.
    It does not save files.
    """

    name = detect_word_name(user_command)
    topic = extract_topic(user_command)
    document_type = detect_document_type(user_command)

    return {
        "success": True,
        "action": "create_ai_word_document",
        "command": user_command,
        "filename": name,
        "topic": topic,
        "document_type": document_type
    }


def create_word_document_from_command(user_command: str):
    """
    This function executes actual Word document creation.
    It should be called by executor.py, not directly by intent_planner.py.
    """

    from app.word_agent.word_live_writer import create_fast_then_live_ai_document

    name = detect_word_name(user_command)
    topic = extract_topic(user_command)
    document_type = detect_document_type(user_command)

    result = create_fast_then_live_ai_document(
        topic=topic,
        filename=name,
        document_type=document_type,
        user_command=user_command
    )

    return result


def handle_word_command(user_command: str):
    """
    Legacy wrapper.
    Kept for compatibility with older code.
    New flow should use create_word_document_from_command().
    """

    if is_word_creation_command(user_command):
        result = create_word_document_from_command(user_command)
        return result.get("message", "Word document created.")

    text = user_command.lower()

    if "analyze current word" in text or "analyze current document" in text:
        path = load_current_document()

        if not path:
            return "No current Word document found."

        doc = read_word_document(path)

        result = analyze_text(
            doc["text"],
            user_command
        )

        if result["success"]:
            append_to_word_document(
                path,
                "Orvix Analysis",
                result["response"]
            )
            return "Analysis added to current Word document."

        return result.get("error", "Analysis failed.")

    if "summarize current word" in text or "summarize current document" in text:
        path = load_current_document()

        if not path:
            return "No current Word document found."

        doc = read_word_document(path)

        result = analyze_text(
            doc["text"],
            "Summarize this document clearly."
        )

        if result["success"]:
            append_to_word_document(
                path,
                "Summary",
                result["response"]
            )
            return "Summary added to current Word document."

        return result.get("error", "Summary failed.")

    return None