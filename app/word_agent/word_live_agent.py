import time
import win32com.client
import pyperclip


def get_word_app():
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = True
    return word


def open_or_create_document(file_path=None):
    word = get_word_app()

    if file_path:
        doc = word.Documents.Open(file_path)
    else:
        doc = word.Documents.Add()

    return word, doc


def insert_paragraph(word, paragraph):
    text = paragraph.strip()

    if not text:
        return

    try:
        pyperclip.copy(text + "\n\n")
        time.sleep(0.1)
        word.Selection.Paste()
    except Exception:
        word.Selection.TypeText(text)
        word.Selection.TypeParagraph()
        word.Selection.TypeParagraph()


def live_insert_text(text, delay=0.15):
    word = get_word_app()

    if word.Documents.Count == 0:
        word.Documents.Add()

    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        insert_paragraph(word, paragraph)
        time.sleep(delay)

    return {
        "success": True,
        "message": "Live text inserted into Word."
    }


def save_active_document(file_path):
    word = get_word_app()

    if word.Documents.Count == 0:
        return {
            "success": False,
            "message": "No active Word document found."
        }

    doc = word.ActiveDocument
    doc.SaveAs(file_path)

    return {
        "success": True,
        "message": f"Saved Word document: {file_path}"
    }