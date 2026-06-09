import re
import win32com.client


def clean_word_text(text: str):
    if not text:
        return ""

    # Word often adds control characters like \r and \x07
    text = text.replace("\r", "\n")
    text = text.replace("\x07", "")
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def get_active_document_text():
    try:
        word = win32com.client.GetActiveObject(
            "Word.Application"
        )

        if word.Documents.Count == 0:
            return {
                "success": False,
                "message": "No active Word document found.",
                "text": "",
                "path": "",
                "name": ""
            }

        doc = word.ActiveDocument

        try:
            path = doc.FullName
        except Exception:
            path = ""

        try:
            name = doc.Name
        except Exception:
            name = ""

        try:
            text = doc.Content.Text
        except Exception:
            text = ""

        return {
            "success": True,
            "message": "Active Word document read successfully.",
            "text": clean_word_text(text),
            "path": path,
            "name": name
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error),
            "text": "",
            "path": "",
            "name": ""
        }