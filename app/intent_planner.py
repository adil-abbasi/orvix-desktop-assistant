import re
from app.word_command_handler import handle_word_command
from app.project_planner import plan_project_request
from app.action_planner import plan_from_project_goal
from app.ai_plan_schema import validate_plan
from app.plan_executor import execute_plan
from app.ai_planner import create_project_plan
from app.project_memory import load_last_project
from app.project_modifier import modify_project
from app.modification_planner import create_modification_plan
from app.modification_code_generator import generate_file_changes
from app.modification_executor import apply_file_changes
from app.word_agent.document_actions import execute_document_action
from app.task_router import route_task
from app.agent_dispatcher import dispatch



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


def is_modify_command(text: str):
    return (
        "modify current project" in text
        or "edit current project" in text
        or "change current project" in text
        or "update current project" in text
        or "add to current project" in text
    )


def handle_modify_current_project(user_command: str):
    project_path = load_last_project()

    if not project_path:
        return "No current project found. Create or open a project first."

    project = modify_project(project_path, user_command)

    if not project.get("success"):
        return project.get("message", "Failed to read current project.")

    plan = create_modification_plan(
        user_command,
        project["project_files"]
    )

    if not plan:
        return "Could not create modification plan."

    changes = generate_file_changes(
        user_command,
        project["project_files"],
        plan
    )

    if not changes:
        return "No file changes were generated."

    result = apply_file_changes(
        project_path,
        changes
    )

    return {
    "success": True,
    "action": "display_message",
    "message": "\n".join(result.get("messages", []))
}


def build_multistep_plan(plan, location, project_name, open_in_vscode):
    steps = [plan]

    if open_in_vscode:
        steps.append({
            "success": True,
            "action": "open_app_in_location",
            "app": "vscode",
            "location": f"{location}\\{project_name}",
            "use_last_created_path": True
        })

    return {
        "success": True,
        "action": "multi_step",
        "steps": steps
    }


def plan_intent(user_command: str):
    text = clean_text(user_command)
    route = route_task(user_command)
    task_type = route["task_type"]

    location = detect_location(text)
    open_in_vscode = wants_vscode(text)

    # 1. Word document creation should return a plan only.
    # It must not open Word here.
    from app.word_command_handler import is_word_creation_command, build_word_creation_plan

    if is_word_creation_command(user_command):
        return build_word_creation_plan(user_command)

    # 2. Existing document actions should also return an executable plan.
    # Example: summarize current document, add section, references, etc.
    word_action_keywords = [
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

    if task_type == "document" or any(keyword in text for keyword in word_action_keywords):
        return {
            "success": True,
            "action": "document_action",
            "command": user_command
        }

    # 3. Modify current project
    if is_modify_command(text):
        return {
            "success": True,
            "action": "modify_current_project",
            "command": user_command
        }

    # 4. AI project generation
    build_words = [
        "build",
        "make",
        "create",
        "generate",
        "banao",
        "banani",
        "banana",
        "chahiye"
    ]

    if any(word in text for word in build_words):
        spec = create_project_plan(user_command)
        spec["location"] = location

        validation = validate_plan(spec)

        if validation["valid"]:
            plan = execute_plan(spec)

            if plan.get("success"):
                return build_multistep_plan(
                    plan,
                    location,
                    spec.get("name", "GeneratedProject"),
                    open_in_vscode
                )

    project_plan = plan_project_request(user_command)

    if project_plan is not None:
        if "planned_plan" in project_plan:
            return project_plan["planned_plan"]

        if "planned_command" in project_plan:
            return project_plan["planned_command"]

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

    if (
        "backend" in text
        or "api" in text
        or "server" in text
        or "express" in text
    ):
        name = detect_project_name(text, "APIBackend")
        return plan_from_project_goal("node express app", name, location, open_in_vscode)

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

    if (
        "django" in text
        or "lms" in text
        or "learning management" in text
        or "admin panel" in text
    ):
        name = detect_project_name(text, "LMS")
        return plan_from_project_goal("django app", name, location, open_in_vscode)

    if (
        "spring boot" in text
        or "java backend" in text
        or "spring project" in text
    ):
        name = detect_project_name(text, "SpringBackend")
        return plan_from_project_goal("spring boot project", name, location, open_in_vscode)

    if (
        "python app" in text
        or "python project" in text
        or "simple python" in text
    ):
        name = detect_project_name(text, "PythonApp")
        return plan_from_project_goal("python app", name, location, open_in_vscode)

    return user_command