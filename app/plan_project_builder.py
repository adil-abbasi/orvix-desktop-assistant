from app.project_generator import generate_blueprint_project


def build_project_from_plan(plan, location="desktop"):

    project_type = plan.get("project_type")
    name = plan.get("name", "GeneratedProject")

    features = plan.get("features", [])
    design_spec = plan.get("design_spec")

    if project_type == "react app":

        return generate_blueprint_project(
            "generic",
            name,
            location,
            features,
            design_spec
        )

    return {
        "success": False,
        "message": f"Unsupported project type: {project_type}"
    }