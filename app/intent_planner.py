import re
from app.project_planner import plan_project_request
from app.action_planner import plan_from_project_goal


def clean_text(text: str):
    
    return text.lower().strip()


def detect_location(text: str):
    location_words = {
        "desktop": ["desktop", "deskstop", "destok", "desktp"],
        "documents": ["documents", "docments", "document", "docs"],
        "downloads": ["downloads", "download", "downlods"],
        "pictures": ["pictures", "images", "photos", "gallery"],
        "music": ["music", "songs"],
        "videos": ["videos", "video"],
    }

    for location, words in location_words.items():
        for word in words:
            if word in text:
                return location

    drive_match = re.search(r"\b([a-zA-Z]:\\[^\n]*)", text)
    if drive_match:
        return drive_match.group(1).strip()

    return "desktop"


def detect_project_name(text: str, default_name: str):
    patterns = [
        r"named\s+([A-Za-z0-9_\-]+)",
        r"name\s+([A-Za-z0-9_\-]+)",
        r"called\s+([A-Za-z0-9_\-]+)",
        r"naam\s+([A-Za-z0-9_\-]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return default_name


def wants_vscode(text: str):
    return (
        "vscode" in text
        or "vs code" in text
        or "visual studio code" in text
        or "code editor" in text
        or "open in code" in text
        or "code mein open" in text
        or "vs code mein open" in text
    )


def plan_intent(user_command: str):
    """
    Returns:
    - dict action plan if natural language intent is detected
    - original string command if no strong intent is detected
    """

    text = clean_text(user_command)
    project_plan = plan_project_request(user_command)

    if project_plan is not None:
        if "planned_plan" in project_plan:
            return project_plan["planned_plan"]

        if "planned_command" in project_plan:
            return project_plan["planned_command"]

   # Website / frontend / portfolio
    if (
        "website" in text
        or "web app" in text
        or "frontend" in text
        or "portfolio" in text
        or "site" in text
        or "webpage" in text
    ):
        name = detect_project_name(text, "Portfolio")
        return plan_from_project_goal("react app", name, location, open_in_vscode)

    # Backend / API
    if (
        "backend" in text
        or "api" in text
        or "server" in text
        or "express" in text
    ):
        name = detect_project_name(text, "APIBackend")
        return plan_from_project_goal("node express app", name, location, open_in_vscode)

    # Machine learning / AI
    if (
        "machine learning" in text
        or "ml project" in text
        or "ai project" in text
        or "prediction" in text
        or "predict" in text
        or "model" in text
        or "dataset" in text
    ):
        name = detect_project_name(text, "MLProject")

        if "disease" in text:
            name = detect_project_name(text, "DiseasePredictor")
        elif "stock" in text:
            name = detect_project_name(text, "StockPredictor")
        elif "hunger" in text:
            name = detect_project_name(text, "HungerPrediction")

        return plan_from_project_goal("ml project", name, location, open_in_vscode)

    # Django / LMS / admin panel
    if (
        "django" in text
        or "lms" in text
        or "learning management" in text
        or "admin panel" in text
    ):
        name = detect_project_name(text, "LMS")
        return plan_from_project_goal("django app", name, location, open_in_vscode)

    # Spring Boot / Java backend
    if (
        "spring boot" in text
        or "java backend" in text
        or "spring project" in text
    ):
        name = detect_project_name(text, "SpringBackend")
        return plan_from_project_goal("spring boot project", name, location, open_in_vscode)

    # Python app
    if (
        "python app" in text
        or "python project" in text
        or "simple python" in text
    ):
        name = detect_project_name(text, "PythonApp")
        return plan_from_project_goal("python app", name, location, open_in_vscode)

    return user_command