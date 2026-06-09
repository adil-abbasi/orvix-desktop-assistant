def is_document_creation_command(user_command):
    text = user_command.lower()

    return (
        ("create" in text or "make" in text or "generate" in text)
        and (
            "word" in text
            or "docx" in text
            or "ms word" in text
            or "word file" in text
            or "word document" in text
        )
    )


def dispatch(task_type, user_command):
    """
    Dispatcher should return executable plans.
    It should not run long tasks directly.
    """

    if task_type == "document":
        if is_document_creation_command(user_command):
            from app.word_command_handler import build_word_creation_plan
            return build_word_creation_plan(user_command)

        return {
            "success": True,
            "action": "document_action",
            "command": user_command
        }

    if task_type == "presentation":
        return {
            "success": True,
            "action": "presentation_task",
            "command": user_command
        }

    if task_type == "spreadsheet":
        return {
            "success": True,
            "action": "spreadsheet_task",
            "command": user_command
        }

    return {
        "success": False,
        "message": "This agent is not connected yet."
    }