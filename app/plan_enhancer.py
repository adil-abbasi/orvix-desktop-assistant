def feature_to_component(feature: str):
    parts = feature.replace("-", "_").replace(" ", "_").split("_")

    return "".join(
        part.capitalize()
        for part in parts
        if part.strip()
    )


def feature_to_route(feature: str):
    cleaned = feature.replace("_", "-").replace(" ", "-").lower().strip("-")

    if cleaned in ["home", "landing", "landing-page"]:
        return "/"

    return "/" + cleaned


def normalize_feature(feature: str):
    return (
        feature.lower()
        .replace("-", "_")
        .replace(" ", "_")
        .strip("_")
    )


def infer_default_features(plan: dict):
    project_type = plan.get("project_type", "").lower()
    name = plan.get("name", "").lower()
    description = plan.get("description", "").lower()
    goal = plan.get("goal", "").lower()
    text = f"{project_type} {name} {description} {goal}"

    if "dashboard" in text or "admin" in text:
        return [
            "dashboard",
            "analytics",
            "users",
            "settings"
        ]

    if "portfolio" in text:
        return [
            "home",
            "about",
            "projects",
            "skills",
            "contact"
        ]

    if "ecommerce" in text or "shop" in text or "store" in text:
        return [
            "home",
            "products",
            "cart",
            "checkout",
            "contact"
        ]

    if "lms" in text or "learning" in text or "course" in text:
        return [
            "home",
            "courses",
            "dashboard",
            "assignments",
            "profile"
        ]

    if "health" in text or "doctor" in text or "medical" in text:
        return [
            "home",
            "services",
            "appointments",
            "doctors",
            "contact"
        ]

    return [
        "home",
        "about",
        "services",
        "features",
        "contact"
    ]


def infer_theme(plan: dict):
    text = " ".join([
        str(plan.get("project_type", "")),
        str(plan.get("name", "")),
        str(plan.get("description", "")),
        str(plan.get("goal", "")),
        " ".join(plan.get("features", []))
    ]).lower()

    if "health" in text or "doctor" in text or "medical" in text:
        return "medical"

    if "business" in text or "company" in text or "startup" in text:
        return "business"

    if "portfolio" in text:
        return "portfolio"

    if "dashboard" in text or "admin" in text:
        return "dashboard"

    if "ai" in text or "machine learning" in text or "tech" in text:
        return "technology"

    return "modern"


def build_default_design_spec(plan: dict):
    theme = infer_theme(plan)

    return {
        "theme": theme,
        "style": "professional",
        "layout": "responsive",
        "tone": "modern and clean",
        "color_scheme": "premium tech",
        "ui_quality": "startup-quality",
        "requirements": [
            "responsive design",
            "clean sections",
            "professional spacing",
            "modern cards",
            "clear navigation",
            "polished landing page"
        ]
    }


def detect_layout(plan: dict):
    features = [normalize_feature(f) for f in plan.get("features", [])]
    theme = plan.get("theme", "default")

    dashboard_words = [
        "dashboard",
        "admin",
        "doctor_dashboard",
        "analytics"
    ]

    if any(feature in dashboard_words for feature in features):
        return "dashboard"

    if theme in ["medical", "business", "technology"]:
        return "professional"

    return "standard"


def detect_dependencies(plan: dict):
    dependencies = []

    if plan.get("project_type") == "react app":
        dependencies.append("react-router-dom")

    features = [normalize_feature(f) for f in plan.get("features", [])]

    if "analytics" in features or "dashboard" in features:
        dependencies.append("recharts")

    return dependencies


def enhance_plan(plan: dict):
    enhanced = dict(plan)

    features = enhanced.get("features", [])

    if not features:
        features = infer_default_features(enhanced)

    features = [normalize_feature(feature) for feature in features]
    enhanced["features"] = features

    if not enhanced.get("design_spec"):
        enhanced["design_spec"] = build_default_design_spec(enhanced)

    if not enhanced.get("theme"):
        enhanced["theme"] = enhanced["design_spec"].get("theme", "modern")

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