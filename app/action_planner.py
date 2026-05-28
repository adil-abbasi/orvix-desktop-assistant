from app.project_templates import PROJECT_TEMPLATES


ALLOWED_ACTIONS = {
    "create_folder",
    "create_file",
    "create_project",
    "open_folder",
    "open_file",
    "open_app",
    "open_app_in_location",
    "copy",
    "move",
    "rename",
    "delete",
    "list_folder",
    "search_file",
    "run_project",
}


RISKY_ACTIONS = {
    "delete",
    "move",
    "rename",
}


def validate_step(step: dict):
    if not isinstance(step, dict):
        return False, "Invalid step format."

    action = step.get("action")

    if action not in ALLOWED_ACTIONS:
        return False, f"Action not allowed: {action}"

    if action == "create_project":
        template = step.get("template")
        if template and template not in PROJECT_TEMPLATES:
            return False, f"Unknown project template: {template}"

    return True, "Step valid."


def validate_plan(plan: dict):
    if not isinstance(plan, dict):
        return False, "Invalid plan format."

    if plan.get("action") != "multi_step":
        return validate_step(plan)

    steps = plan.get("steps", [])

    if not isinstance(steps, list) or not steps:
        return False, "Plan has no steps."

    for step in steps:
        valid, message = validate_step(step)
        if not valid:
            return False, message

    return True, "Plan valid."


def plan_from_project_goal(template: str, name: str, location: str, open_in_vscode: bool = True):
    if template not in PROJECT_TEMPLATES:
        return {
            "success": False,
            "message": f"Unknown project template: {template}"
        }

    template_data = PROJECT_TEMPLATES[template]

    steps = [
        {
            "success": True,
            "action": "create_project",
            "name": name,
            "location": location,
            "template": template,
            "folders": template_data["folders"],
            "files": template_data["files"]
        }
    ]

    if open_in_vscode:
        steps.append({
            "success": True,
            "action": "open_app_in_location",
            "app": "vscode",
            "location": f"{location}\\{name}",
            "use_last_created_path": True
        })

    plan = {
        "success": True,
        "action": "multi_step",
        "steps": steps
    }

    valid, message = validate_plan(plan)

    if not valid:
        return {
            "success": False,
            "message": message
        }

    return plan


def plan_from_simple_action(action: str, **kwargs):
    step = {
        "success": True,
        "action": action,
        **kwargs
    }

    valid, message = validate_step(step)

    if not valid:
        return {
            "success": False,
            "message": message
        }

    return step