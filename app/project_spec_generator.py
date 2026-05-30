import re


PROJECT_TYPES = {
    "website": "react app",
    "web app": "react app",
    "frontend": "react app",
    "dashboard": "react app",
    "portal": "react app",
    "system": "react app",
    "ml": "ml project",
    "machine learning": "ml project",
    "prediction": "ml project",
    "api": "node express app",
    "backend": "node express app",
}


THEMES = {
    "dark": ["dark", "black theme", "dark ui"],
    "light": ["light", "clean"],
    "medical": ["hospital", "doctor", "patient", "clinic"],
    "education": ["lms", "student", "teacher", "course"],
    "business": ["business", "crm", "admin"],
}


def normalize_feature_name(text: str):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s_]", "", text)
    text = text.replace(" ", "_")
    return text


def detect_project_type(text: str):
    lower = text.lower()

    for keyword, project_type in PROJECT_TYPES.items():
        if keyword in lower:
            return project_type

    return "react app"


def detect_theme(text: str):
    lower = text.lower()

    for theme, keywords in THEMES.items():
        for keyword in keywords:
            if keyword in lower:
                return theme

    return "default"


def detect_project_name(text: str, default_name="GeneratedProject"):
    patterns = [
        r"named\s+([A-Za-z0-9_\-]+)",
        r"name\s+([A-Za-z0-9_\-]+)",
        r"called\s+([A-Za-z0-9_\-]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)

    if "hospital" in text.lower():
        return "HospitalWebsite"
    if "ecommerce" in text.lower() or "shop" in text.lower():
        return "EcommerceWebsite"
    if "portfolio" in text.lower():
        return "PortfolioWebsite"
    if "lms" in text.lower():
        return "LMSWebsite"

    return default_name


def extract_features(text: str):
    lower = text.lower()

    known_features = [
        "doctor dashboard",
        "patient records",
        "appointments",
        "login",
        "dashboard",
        "products",
        "cart",
        "checkout",
        "contact",
        "profile",
        "settings",
        "notifications",
        "analytics"
    ]

    found = []

    for feature in known_features:
        if feature in lower:
            found.append(
                normalize_feature_name(feature)
            )
    if "doctor_dashboard" in found and "dashboard" in found:
        found.remove("dashboard")
        
    return found

def generate_project_spec(user_text: str):
    return {
        "project_type": detect_project_type(user_text),
        "name": detect_project_name(user_text),
        "features": extract_features(user_text),
        "theme": detect_theme(user_text),
        "raw_request": user_text
    }