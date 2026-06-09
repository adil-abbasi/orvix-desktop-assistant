from app.progress_manager import progress_manager
from app.word_agent.word_content_generator import stream_document_from_user_command
from app.word_agent.word_memory import save_current_document
from app.word_agent.word_creator import get_desktop_path, get_unique_file_path
from app.word_agent.word_live_agent import (
    open_or_create_document,
    live_insert_text,
    stream_insert_text_chunks,
    save_active_document
)


def create_fast_then_live_ai_document(
    topic,
    filename,
    document_type="document",
    user_command=None
):
    desktop = get_desktop_path()

    if not filename.lower().endswith(".docx"):
        filename = f"{filename}.docx"

    file_path = get_unique_file_path(desktop, filename)

    progress_manager.update("Opening Microsoft Word...")
    open_or_create_document()

    progress_manager.update("Microsoft Word is ready.")

    live_insert_text(
        f"{topic.title()}\n\nPreparing AI content...\n\n",
        delay=0.008,
        chunk_size=6
    )

    save_active_document(file_path)
    save_current_document(file_path)

    progress_manager.update("AI is writing live into Word...")

    chunks = stream_document_from_user_command(
        user_command=user_command or topic,
        topic=topic,
        document_type=document_type
    )

    stream_insert_text_chunks(
        chunks,
        delay=0.006,
        chunk_size=6
    )

    progress_manager.update("Saving document...")
    save_active_document(file_path)

    progress_manager.update("Task completed.")

    return {
        "success": True,
        "path": file_path,
        "message": f"Document completed: {file_path}"
    }


def create_structured_docx_then_open(
    topic,
    filename,
    document_type="document",
    user_command=None
):
    return create_fast_then_live_ai_document(
        topic=topic,
        filename=filename,
        document_type=document_type,
        user_command=user_command
    )