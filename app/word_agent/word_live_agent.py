import time
import re
import win32com.client

WORD_APP = None


def get_word_app():
    global WORD_APP

    if WORD_APP is None:
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
        doc = word.Documents.Open(file_path)
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
    Fast but visible Word typing.
    Small chunks make it visible.
    Delay keeps Word from looking like instant paste.
    """

    if not text:
        return

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


def live_insert_text(text, delay=0.015, chunk_size=5):
    word = get_word_app()

    if word.Documents.Count == 0:
        word.Documents.Add()

    for line in text.split("\n"):
        clean_line = line.strip()

        if not clean_line:
            word.Selection.TypeParagraph()
            continue

        type_visible_text(
            word=word,
            text=clean_line,
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

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            word.Selection.TypeParagraph()
            continue

        if line.startswith("# "):
            word.Selection.Style = "Title"
            clean_line = line.replace("# ", "", 1)

        elif line.startswith("## "):
            word.Selection.Style = "Heading 1"
            clean_line = line.replace("## ", "", 1)

        elif line.startswith("### "):
            word.Selection.Style = "Heading 2"
            clean_line = line.replace("### ", "", 1)

        elif line.startswith("- "):
            word.Selection.Style = "List Paragraph"
            clean_line = "• " + line.replace("- ", "", 1)

        else:
            word.Selection.Style = "Normal"
            clean_line = line

        if live:
            type_visible_text(
                word=word,
                text=clean_line,
                delay=delay,
                chunk_size=chunk_size
            )
        else:
            word.Selection.TypeText(clean_line)

        word.Selection.TypeParagraph()

    return {
        "success": True,
        "message": "Structured text inserted."
    }

def stream_insert_text_chunks(chunks, delay=0.006, chunk_size=6):
    """
    Stream AI chunks directly into Microsoft Word.
    This allows Word to start writing while AI is still generating.
    """

    word = get_word_app()

    if word.Documents.Count == 0:
        word.Documents.Add()

    buffer = ""

    for incoming_text in chunks:
        if not incoming_text:
            continue

        buffer += incoming_text

        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            line = line.strip()

            if not line:
                word.Selection.TypeParagraph()
                continue

            # Basic heading detection
            if re.match(r"^\d+\.\s+", line):
                word.Selection.Style = "Heading 1"
            elif line.endswith(":") and len(line) < 80:
                word.Selection.Style = "Heading 1"
            else:
                word.Selection.Style = "Normal"

            type_visible_text(
                word=word,
                text=line,
                delay=delay,
                chunk_size=chunk_size
            )

            word.Selection.TypeParagraph()

    # Write remaining buffer
    if buffer.strip():
        word.Selection.Style = "Normal"

        type_visible_text(
            word=word,
            text=buffer.strip(),
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

    word.Selection.TypeText(text)

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

    try:
        doc.SaveAs2(file_path)
    except Exception:
        doc.SaveAs(file_path)

    return {
        "success": True,
        "message": f"Saved Word document: {file_path}"
    }