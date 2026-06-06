import re

from app.word_agent.word_creator import create_word_document
from app.word_agent.word_memory import load_current_document
from app.word_agent.word_reader import read_word_document
from app.word_agent.word_analyzer import analyze_text
from app.word_agent.word_writer import append_to_word_document
from app.word_agent.word_content_generator import generate_document_content


def detect_word_name(text, default_name="OrvixDocument"):
    match = re.search(r"named\s+([A-Za-z0-9_\-]+)", text, re.IGNORECASE)

    if match:
        return match.group(1)

    match = re.search(r"name\s+([A-Za-z0-9_\-]+)", text, re.IGNORECASE)

    if match:
        return match.group(1)

    return default_name


def extract_topic(text):
    match = re.search(r"about\s+(.+)", text, re.IGNORECASE)

    if match:
        topic = match.group(1).strip()
        return topic

    match = re.search(r"on\s+(.+)", text, re.IGNORECASE)

    if match:
        topic = match.group(1).strip()
        return topic

    return text


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

    if "notes" in text:
        return "study notes"

    return "report"


def handle_word_command(user_command: str):
    text = user_command.lower()

    if "create" in text and ("word" in text or "docx" in text or "ms word" in text):
        name = detect_word_name(user_command)
        topic = extract_topic(user_command)
        document_type = detect_document_type(user_command)

        title = topic.title()

        content = generate_document_content(
            topic=topic,
            document_type=document_type
        )

        result = create_word_document(
            name=name,
            title=title,
            content=content,
            open_file=True
        )

        return result["message"]

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