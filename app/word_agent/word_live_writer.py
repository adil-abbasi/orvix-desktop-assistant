import os

from app.word_agent.word_content_generator import generate_document_content
from app.word_agent.word_live_agent import open_or_create_document, live_insert_text, save_active_document
from app.word_agent.word_memory import save_current_document
from app.word_agent.word_creator import get_desktop_path


def create_live_ai_document(topic, filename, document_type="report"):
    desktop = get_desktop_path()

    if not filename.lower().endswith(".docx"):
        filename = f"{filename}.docx"

    file_path = os.path.join(desktop, filename)

    content = generate_document_content(
        topic=topic,
        document_type=document_type
    )

    open_or_create_document()

    live_insert_text(
        f"{topic.title()}\n\n{content}",
        delay=0.15
    )

    save_active_document(file_path)
    save_current_document(file_path)

    return {
        "success": True,
        "path": file_path,
        "message": f"Live Word document created: {file_path}"
    }