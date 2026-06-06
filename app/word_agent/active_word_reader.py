import win32com.client


def get_active_document_text():
    try:
        word = win32com.client.GetActiveObject(
            "Word.Application"
        )

        if word.Documents.Count == 0:
            return {
                "success": False,
                "response": "No active document."
            }

        doc = word.ActiveDocument

        return {
            "success": True,
            "text": doc.Content.Text
        }

    except Exception as error:
        return {
            "success": False,
            "response": str(error)
        }