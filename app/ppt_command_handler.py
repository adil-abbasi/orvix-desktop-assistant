import re
from app.ppt_agent.ppt_creator import create_presentation

def is_ppt_creation_command(user_command: str):
    text = user_command.lower().strip()

    ppt_words = [
        "ppt",
        "powerpoint",
        "presentation",
        "slides",
        "slide deck"
    ]

    create_words = [
        "create",
        "make",
        "generate",
        "build",
        "banao",
        "banani",
        "banana"
    ]

    return (
        any(word in text for word in ppt_words)
        and any(word in text for word in create_words)
    )


def detect_ppt_name(user_command: str):
    patterns = [
        r"named\s+([A-Za-z0-9_\- ]+?)\s+about",
        r"name\s+([A-Za-z0-9_\- ]+?)\s+about",
        r"called\s+([A-Za-z0-9_\- ]+?)\s+about",
        r"naam\s+([A-Za-z0-9_\- ]+?)\s+about",
        r"named\s+([A-Za-z0-9_\- ]+)",
        r"name\s+([A-Za-z0-9_\- ]+)",
        r"called\s+([A-Za-z0-9_\- ]+)",
        r"naam\s+([A-Za-z0-9_\- ]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, user_command, flags=re.IGNORECASE)

        if match:
            name = match.group(1).strip()
            name = re.sub(r"\s+", "_", name)
            return name

    return "Orvix_Presentation"


def detect_ppt_topic(user_command: str):
    patterns = [
        r"about\s+(.+)",
        r"on\s+(.+)",
        r"topic\s+(.+)",
        r"regarding\s+(.+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, user_command, flags=re.IGNORECASE)

        if match:
            topic = match.group(1).strip()

            topic = re.sub(
                r"\b(in|on|at)\s+(desktop|documents|downloads)\b",
                "",
                topic,
                flags=re.IGNORECASE
            )

            topic = re.sub(
                r"\b\d+\s+slides?\b",
                "",
                topic,
                flags=re.IGNORECASE
            )

            return topic.strip()

    return "Artificial Intelligence"


def detect_slide_count(user_command: str):
    match = re.search(r"(\d+)\s+slides?", user_command, flags=re.IGNORECASE)

    if match:
        count = int(match.group(1))

        if count < 3:
            return 3

        if count > 15:
            return 15

        return count

    return 6


def detect_location(user_command: str):
    text = user_command.lower()

    if "documents" in text or "document" in text:
        return "documents"

    if "downloads" in text or "download" in text:
        return "downloads"

    return "desktop"


def build_ppt_creation_plan(user_command: str):
    name = detect_ppt_name(user_command)
    topic = detect_ppt_topic(user_command)
    slide_count = detect_slide_count(user_command)
    location = detect_location(user_command)

    return {
        "success": True,
        "action": "create_ai_ppt",
        "command": user_command,
        "filename": name,
        "topic": topic,
        "slide_count": slide_count,
        "location": location
    }


def create_ppt_from_command(user_command: str):
    from app.ppt_agent.ppt_creator import create_presentation

    plan = build_ppt_creation_plan(user_command)

    return create_presentation(
        topic=plan["topic"],
        filename=plan["filename"],
        slide_count=plan["slide_count"],
        location=plan["location"],
        user_command=user_command
    )