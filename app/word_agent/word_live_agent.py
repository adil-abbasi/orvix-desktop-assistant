import time
import re
from pathlib import Path

import win32com.client


WORD_APP = None


def get_word_app():
    global WORD_APP

    try:
        if WORD_APP is None:
            WORD_APP = win32com.client.Dispatch("Word.Application")
    except Exception:
        WORD_APP = win32com.client.Dispatch("Word.Application")

    WORD_APP.Visible = True
    WORD_APP.WindowState = 1

    try:
        WORD_APP.ScreenUpdating = True
    except Exception:
        pass

    try:
        WORD_APP.Activate()
    except Exception:
        pass

    return WORD_APP


def open_or_create_document(file_path=None):
    word = get_word_app()

    if file_path:
        doc = word.Documents.Open(str(file_path))
    else:
        doc = word.Documents.Add()

    try:
        word.ActiveWindow.Activate()
    except Exception:
        pass

    try:
        word.Selection.EndKey(Unit=6)
    except Exception:
        pass

    return word, doc


def type_visible_text(word, text, delay=0.018, chunk_size=5):
    """
    Types text into Word in visible small chunks.
    """

    if not text:
        return

    text = str(text)

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]

        try:
            word.Selection.TypeText(chunk)
        except Exception:
            time.sleep(0.15)
            word.Selection.TypeText(chunk)

        try:
            word.ScreenRefresh()
        except Exception:
            pass

        if delay and delay > 0:
            time.sleep(delay)


def apply_line_style(word, line: str):
    """
    Applies simple Word styling based on line type.
    Keeps formatting safe and readable.
    """

    clean_line = line.strip()

    if not clean_line:
        return ""

    # Title-like lines
    if len(clean_line) < 70 and not clean_line.endswith("."):
        lower_line = clean_line.lower()

        heading_words = [
            "introduction",
            "summary",
            "key concepts",
            "applications",
            "benefits",
            "advantages",
            "disadvantages",
            "examples",
            "study notes",
            "conclusion",
            "multiple choice questions",
            "mcqs",
            "references"
        ]

        if lower_line in heading_words:
            try:
                word.Selection.Style = "Heading 1"
            except Exception:
                pass
            return clean_line

    # Numbered headings like 1. Introduction
    if re.match(r"^\d+\.\s+[A-Za-z].*", clean_line) and len(clean_line) < 90:
        try:
            word.Selection.Style = "Heading 1"
        except Exception:
            pass
        return clean_line

    # Lines ending with colon are usually headings
    if clean_line.endswith(":") and len(clean_line) < 80:
        try:
            word.Selection.Style = "Heading 1"
        except Exception:
            pass
        return clean_line

    # Bullet lines
    if clean_line.startswith("- "):
        try:
            word.Selection.Style = "List Paragraph"
        except Exception:
            pass
        return "• " + clean_line[2:].strip()

    # MCQ options should remain normal
    if re.match(r"^[A-D]\.\s+", clean_line):
        try:
            word.Selection.Style = "Normal"
        except Exception:
            pass
        return clean_line

    # Answer lines can be bold-ish style impossible safely without extra range,
    # so keep normal for stability.
    if clean_line.lower().startswith("answer:"):
        try:
            word.Selection.Style = "Normal"
        except Exception:
            pass
        return clean_line

    try:
        word.Selection.Style = "Normal"
    except Exception:
        pass

    return clean_line


def live_insert_text(text, delay=0.015, chunk_size=5):
    word = get_word_app()

    if word.Documents.Count == 0:
        word.Documents.Add()

    text = str(text or "")

    for line in text.split("\n"):
        clean_line = line.strip()

        if not clean_line:
            word.Selection.TypeParagraph()
            continue

        styled_line = apply_line_style(word, clean_line)

        type_visible_text(
            word=word,
            text=styled_line,
            delay=delay,
            chunk_size=chunk_size
        )

        word.Selection.TypeParagraph()

    return {
        "success": True,
        "message": "Live text inserted into Word."
    }


def insert_structured_text(
    text,
    live=True,
    delay=0.015,
    chunk_size=5
):
    word = get_word_app()

    if word.Documents.Count == 0:
        word.Documents.Add()

    text = str(text or "")

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            word.Selection.TypeParagraph()
            continue

        styled_line = apply_line_style(word, line)

        if live:
            type_visible_text(
                word=word,
                text=styled_line,
                delay=delay,
                chunk_size=chunk_size
            )
        else:
            word.Selection.TypeText(styled_line)

        word.Selection.TypeParagraph()

    return {
        "success": True,
        "message": "Structured text inserted."
    }


def stream_insert_text_chunks(chunks, delay=0.006, chunk_size=6):
    """
    Streams AI/fallback chunks directly into Microsoft Word.
    If Gemini fails, fallback text still writes safely.
    """

    word = get_word_app()

    if word.Documents.Count == 0:
        word.Documents.Add()

    buffer = ""

    for incoming_text in chunks:
        if not incoming_text:
            continue

        buffer += str(incoming_text)

        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.strip()

            if not line:
                word.Selection.TypeParagraph()
                continue

            styled_line = apply_line_style(word, line)

            type_visible_text(
                word=word,
                text=styled_line,
                delay=delay,
                chunk_size=chunk_size
            )

            word.Selection.TypeParagraph()

    if buffer.strip():
        styled_line = apply_line_style(word, buffer.strip())

        type_visible_text(
            word=word,
            text=styled_line,
            delay=delay,
            chunk_size=chunk_size
        )

        word.Selection.TypeParagraph()

    return {
        "success": True,
        "message": "Streamed text inserted into Word."
    }


def fast_insert_text(text):
    word = get_word_app()

    if word.Documents.Count == 0:
        word.Documents.Add()

    word.Selection.TypeText(str(text or ""))

    return {
        "success": True,
        "message": "Text inserted fast."
    }


def save_active_document(file_path):
    word = get_word_app()

    if word.Documents.Count == 0:
        return {
            "success": False,
            "message": "No active Word document found."
        }

    doc = word.ActiveDocument
    file_path = Path(file_path)

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    try:
        doc.SaveAs2(str(file_path))
    except Exception:
        doc.SaveAs(str(file_path))

    return {
        "success": True,
        "message": f"Saved Word document: {file_path}"
    }