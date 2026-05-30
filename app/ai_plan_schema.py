REQUIRED_FIELDS = [
    "project_type",
    "name",
    "features",
    "theme"
]


VALID_PROJECT_TYPES = [
    "react app",
    "ml project",
    "node express app",
    "django app",
    "flask app",
    "spring boot app"
]


def validate_plan(plan: dict):
    errors = []

    for field in REQUIRED_FIELDS:
        if field not in plan:
            errors.append(f"Missing field: {field}")

    project_type = plan.get("project_type")

    if project_type not in VALID_PROJECT_TYPES:
        errors.append(
            f"Unsupported project type: {project_type}"
        )

    features = plan.get("features", [])

    if not isinstance(features, list):
        errors.append(
            "features must be a list"
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }