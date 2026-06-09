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
    # 2. PowerPoint / PPT creation should go to PPT agent.
from app.ppt_command_handler import is_ppt_creation_command, build_ppt_creation_plan



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

def is_normal_system_command(text: str):
    starters = [
        "create folder",
        "create a folder",
        "create file",
        "create text file",
        "create python file",
        "create excel file",
        "create powerpoint file",
        "create presentation",
        "create spreadsheet",
        "open app",
        "open folder",
        "open file",
        "open ",
        "copy ",
        "move ",
        "cut ",
        "rename ",
        "delete ",
        "remove ",
        "list ",
        "search "
    ]

    return any(text.startswith(starter) for starter in starters)


def is_project_generation_candidate(text: str):
    project_keywords = [
        "project",
        "app",
        "website",
        "web app",
        "frontend",
        "backend",
        "api",
        "react",
        "django",
        "flask",
        "spring boot",
        "node",
        "express",
        "machine learning",
        "ml project",
        "ai project",
        "prediction",
        "portfolio",
        "lms"
    ]

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

    return (
        any(word in text for word in build_words)
        and any(keyword in text for keyword in project_keywords)
    )
def plan_intent(user_command: str):
    text = clean_text(user_command)
    route = route_task(user_command)
    task_type = route["task_type"]

    location = detect_location(text)
    open_in_vscode = wants_vscode(text)

    # 1. Word document creation should go to Word AI agent.
    # It must not open Word here; it only returns a plan.
    from app.word_command_handler import is_word_creation_command, build_word_creation_plan

    if is_word_creation_command(user_command):
        return build_word_creation_plan(user_command)

    # 2. PowerPoint / PPT creation should go to PPT agent.
    from app.ppt_command_handler import is_ppt_creation_command, build_ppt_creation_plan

    if is_ppt_creation_command(user_command):
        return build_ppt_creation_plan(user_command)
    # 2. Normal desktop/file/app commands should go directly to command_parser.
    # Do not send these to AI planner.
    if is_normal_system_command(text):
        return user_command

    # 3. Existing document modification actions.
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

    # 4. Modify current project.
    if is_modify_command(text):
        return {
            "success": True,
            "action": "modify_current_project",
            "command": user_command
        }

    # 5. React / website / frontend project generation.
    if (
        "website" in text
        or "web app" in text
        or "frontend" in text
        or "portfolio" in text
        or "site" in text
        or "webpage" in text
        or "react" in text
    ):
        name = detect_project_name(text, "Portfolio")

        local_plan = {
            "project_type": "react app",
            "name": name,
            "location": location,
            "features": [],
            "design_spec": None
        }

        plan = execute_plan(local_plan)

        if plan.get("success"):
            return build_multistep_plan(
                plan,
                location,
                name,
                open_in_vscode
            )

        return plan_from_project_goal("react app", name, location, open_in_vscode)

    # 6. Backend / Node / Express project.
    if (
        "backend" in text
        or "api" in text
        or "server" in text
        or "express" in text
        or "node" in text
    ):
        name = detect_project_name(text, "APIBackend")
        return plan_from_project_goal("node express app", name, location, open_in_vscode)

    # 7. Machine learning / AI / prediction project.
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

    # 8. Django / LMS project.
    if (
        "django" in text
        or "lms" in text
        or "learning management" in text
        or "admin panel" in text
    ):
        name = detect_project_name(text, "LMS")
        return plan_from_project_goal("django app", name, location, open_in_vscode)

    # 9. Spring Boot project.
    if (
        "spring boot" in text
        or "java backend" in text
        or "spring project" in text
    ):
        name = detect_project_name(text, "SpringBackend")
        return plan_from_project_goal("spring boot project", name, location, open_in_vscode)

    # 10. Python project.
    if (
        "python app" in text
        or "python project" in text
        or "simple python" in text
    ):
        name = detect_project_name(text, "PythonApp")
        return plan_from_project_goal("python app", name, location, open_in_vscode)

    # 11. AI project generation only for real project/app requests.
    # This must not catch simple commands like create folder/file.
    if is_project_generation_candidate(text):
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

    # 12. Old project planner fallback.
    project_plan = plan_project_request(user_command)

    if project_plan is not None:
        if "planned_plan" in project_plan:
            return project_plan["planned_plan"]

        if "planned_command" in project_plan:
            return project_plan["planned_command"]

    return user_command