import re

from app.word_agent.word_memory import load_current_document
from app.word_agent.word_reader import read_word_document
from app.word_agent.word_analyzer import analyze_text
from app.word_agent.word_writer import append_to_word_document


def clean_filename(name: str):
    name = name.strip()

    if not name:
        return "OrvixDocument"

    blocked_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

    for char in blocked_chars:
        name = name.replace(char, "")

    name = re.sub(r"\s+", "_", name)

    return name or "OrvixDocument"


def detect_word_name(text, default_name="OrvixDocument"):
    patterns = [
        r"named\s+([A-Za-z0-9_\- ]+?)\s+about",
        r"name\s+([A-Za-z0-9_\- ]+?)\s+about",
        r"called\s+([A-Za-z0-9_\- ]+?)\s+about",
        r"naam\s+([A-Za-z0-9_\- ]+?)\s+about",
        r"named\s+([A-Za-z0-9_\- ]+?)\s+on",
        r"name\s+([A-Za-z0-9_\- ]+?)\s+on",
        r"called\s+([A-Za-z0-9_\- ]+?)\s+on",
        r"naam\s+([A-Za-z0-9_\- ]+?)\s+on",
        r"named\s+([A-Za-z0-9_\- ]+)",
        r"name\s+([A-Za-z0-9_\- ]+)",
        r"called\s+([A-Za-z0-9_\- ]+)",
        r"naam\s+([A-Za-z0-9_\- ]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return clean_filename(match.group(1))

    return clean_filename(default_name)


def clean_topic(topic: str):
    topic = topic.strip()

    topic = re.sub(
        r"\b(in|on|at)\s+(desktop|documents|downloads)\b",
        "",
        topic,
        flags=re.IGNORECASE
    )

    topic = re.sub(
        r"\b\d+\s+(pages?|words?)\b",
        "",
        topic,
        flags=re.IGNORECASE
    )

    topic = topic.strip(" .,-")

    return topic or "Generated Document"


def extract_topic(text):
    patterns = [
        r"about\s+(.+)",
        r"on\s+(.+)",
        r"topic\s+(.+)",
        r"regarding\s+(.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return clean_topic(match.group(1))

    name = detect_word_name(text, "")

    if name:
        return clean_topic(name.replace("_", " "))

    return clean_topic(text)


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

    if "mcq" in text or "mcqs" in text:
        return "mcqs"

    if "examples" in text or "example" in text:
        return "examples"

    if "advantages" in text or "disadvantages" in text or "benefits" in text:
        return "advantages and disadvantages"

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
    text = user_command.lower().strip()

    create_words = [
        "create",
        "make",
        "generate",
        "build",
        "banao",
        "banani",
        "banana"
    ]

    word_words = [
        "word",
        "docx",
        "ms word",
        "word file",
        "word document",
        "doc file",
        "document file"
    ]

    return (
        any(word in text for word in create_words)
        and any(word in text for word in word_words)
    )


def build_word_creation_plan(user_command: str):
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