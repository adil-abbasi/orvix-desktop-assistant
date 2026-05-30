from app.project_generator import generate_blueprint_project


def build_project_from_plan(plan: dict, location="desktop"):
    project_type = plan.get("project_type")
    name = plan.get("name", "GeneratedProject")
    features = plan.get("features", [])

    if project_type == "react app":
        return generate_blueprint_project(
            "generic",
            name,
            location,
            features
        )

    return {
        "success": False,
        "message": f"Plan-driven build not supported yet for: {project_type}"
    }