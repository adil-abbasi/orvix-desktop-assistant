def dispatch(task_type, user_command):
    if task_type == "document":
        from app.word_agent.document_actions import execute_document_action
        return execute_document_action(user_command)

    if task_type == "project":
        return {
            "success": True,
            "message": "Project agent not connected yet."
        }

    if task_type == "project_modification":
        return {
            "success": True,
            "message": "Project modification agent not connected yet."
        }

    if task_type == "presentation":
        return {
            "success": True,
            "message": "Presentation agent not connected yet."
        }

    if task_type == "spreadsheet":
        return {
            "success": True,
            "message": "Spreadsheet agent not connected yet."
        }

    return {
        "success": False,
        "message": "Unknown task type."
    }