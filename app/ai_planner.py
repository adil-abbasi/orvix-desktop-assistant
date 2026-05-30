from app.project_spec_generator import generate_project_spec


def create_project_plan(user_request: str):
    return generate_project_spec(user_request)