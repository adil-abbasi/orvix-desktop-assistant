def feature_to_component(feature: str):
    parts = feature.replace("-", "_").split("_")

    return "".join(
        part.capitalize()
        for part in parts
        if part.strip()
    )


def feature_to_route(feature: str):
    return "/" + feature.replace("_", "-").replace(" ", "-").lower()


def detect_layout(plan: dict):
    features = plan.get("features", [])
    theme = plan.get("theme", "default")

    dashboard_words = [
        "dashboard",
        "admin",
        "doctor_dashboard",
        "analytics"
    ]

    if any(feature in dashboard_words for feature in features):
        return "dashboard"

    if theme in ["medical", "business"]:
        return "professional"

    return "standard"


def detect_dependencies(plan: dict):
    dependencies = []

    if plan.get("project_type") == "react app":
        dependencies.append("react-router-dom")

    features = plan.get("features", [])

    if "analytics" in features:
        dependencies.append("recharts")

    return dependencies


def enhance_plan(plan: dict):
    enhanced = dict(plan)

    features = enhanced.get("features", [])

    pages = []

    for feature in features:
        component = feature_to_component(feature)

        pages.append({
            "feature": feature,
            "component": component,
            "file": f"src/pages/{component}.jsx",
            "route": feature_to_route(feature)
        })

    enhanced["pages"] = pages
    enhanced["layout"] = detect_layout(enhanced)
    enhanced["dependencies"] = detect_dependencies(enhanced)

    return enhanced