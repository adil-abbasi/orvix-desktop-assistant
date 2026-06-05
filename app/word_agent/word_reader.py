from docx import Document


def read_word_document(file_path):
    document = Document(file_path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    full_text = "\n".join(paragraphs)

    return {
        "success": True,
        "text": full_text,
        "paragraphs": len(paragraphs),
        "words": len(full_text.split())
    }