from app.project_generator import generate_blueprint_project


def execute_plan(plan):
    project_type = plan.get("project_type")
    name = plan.get("name")
    features = plan.get("features", [])

    if project_type == "react app":
        return generate_blueprint_project(
            "react",
            name,
            "desktop",
            features
        )

    if project_type == "ml project":
        return generate_blueprint_project(
            "ml",
            name,
            "desktop",
            features
        )

    return {
        "success": False,
        "message": f"Unsupported project type: {project_type}"
    }