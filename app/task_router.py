def detect_task_type(user_command: str):
    text = user_command.lower().strip()

    modification_keywords = [
        "modify current project",
        "edit current project",
        "change current project",
        "update current project",
        "add to current project"
    ]

    presentation_keywords = [
        "powerpoint",
        "ppt",
        "presentation",
        "slides"
    ]

    spreadsheet_keywords = [
        "excel",
        "spreadsheet",
        "sheet",
        "dashboard"
    ]

    document_keywords = [
        "word",
        "docx",
        "ms word",
        "mcq",
        "mcqs",
        "viva",
        "summarize",
        "summary",
        "paraphrase",
        "rewrite",
        "references",
        "reference",
        "conclusion",
        "continue writing",
        "add section",
        "executive summary",
        "study notes"
    ]

    project_keywords = [
        "build",
        "create project",
        "make project",
        "generate project",
        "react",
        "website",
        "web app",
        "ml project",
        "machine learning",
        "django",
        "flask",
        "spring boot",
        "node",
        "express"
    ]

    if any(keyword in text for keyword in modification_keywords):
        return "project_modification"

    if any(keyword in text for keyword in presentation_keywords):
        return "presentation"

    if any(keyword in text for keyword in spreadsheet_keywords):
        return "spreadsheet"

    if any(keyword in text for keyword in document_keywords):
        return "document"

    if any(keyword in text for keyword in project_keywords):
        return "project"

    return "unknown"


def route_task(user_command: str):
    task_type = detect_task_type(user_command)

    return {
        "task_type": task_type,
        "command": user_command
    }