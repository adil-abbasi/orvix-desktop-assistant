from app.project_spec_generator import generate_project_spec


def ai_available():
    return False


def create_project_plan(user_request: str):
    """
    Future:
    AI Planner
    ↓
    JSON Plan

    Current:
    Rule-Based Planner
    """

    if ai_available():
        return create_ai_plan(user_request)

    return generate_project_spec(user_request)


def create_ai_plan(user_request: str):
    raise NotImplementedError(
        "AI planner not connected yet."
    )