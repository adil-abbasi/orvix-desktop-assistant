from email.mime import text
import re
from app.project_generator import generate_blueprint_project
from app.feature_composer import detect_features
PROJECT_KNOWLEDGE = {
    "ecommerce": {
        "name": "EcommerceWebsite",
        "template": "react app",
        "features": ["products", "cart", "checkout", "admin dashboard"]
    },
    "shop": {
        "name": "ShopWebsite",
        "template": "react app",
        "features": ["products", "cart", "checkout"]
    },
    "portfolio": {
        "name": "Portfolio",
        "template": "react app",
        "features": ["home", "about", "projects", "contact"]
    },
    "hospital": {
        "name": "HospitalManagement",
        "template": "react app",
        "features": ["patients", "doctors", "appointments", "dashboard"]
    },
    "lms": {
        "name": "LearningManagementSystem",
        "template": "react app",
        "features": ["students", "teachers", "courses", "assignments"]
    },
    "student": {
        "name": "StudentPortal",
        "template": "react app",
        "features": ["students", "courses", "dashboard"]
    },
}


def detect_location(text: str):
    text = text.lower()

    if "documents" in text or "docments" in text:
        return "documents"
    if "downloads" in text:
        return "downloads"
    if "desktop" in text or "deskstop" in text or "destok" in text:
        return "desktop"

    return "desktop"


def detect_project_name(text: str, default_name: str):
    patterns = [
        r"named\s+([A-Za-z0-9_\-]+)",
        r"name\s+([A-Za-z0-9_\-]+)",
        r"called\s+([A-Za-z0-9_\-]+)",
        r"naam\s+([A-Za-z0-9_\-]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return default_name


def wants_vscode(text: str):
    text = text.lower()
    return (
        "vscode" in text
        or "vs code" in text
        or "visual studio code" in text
        or "code mein open" in text
        or "code main open" in text
    )


def plan_project_request(user_text: str):
    text = user_text.lower().strip()

    build_words = ["build", "make", "create", "generate", "banao", "banani", "banana", "chahiye"]

    if not any(word in text for word in build_words):
        return None

    for keyword, data in PROJECT_KNOWLEDGE.items():
        if keyword in text:
            location = detect_location(text)
            name = detect_project_name(text, data["name"])

            open_in_vscode = wants_vscode(text)
            custom_features = detect_features(text)
            custom_features = detect_features(text)
            command = f"create {data['template']} {name} in {location}"

            if open_in_vscode:
                command += " and open it in vscode"
            else:
                command += " and open it"
        print("DEBUG FEATURES:", custom_features)
        blueprint_plan = generate_blueprint_project(keyword, name, location, custom_features)

        if not blueprint_plan["success"]:
            return None

        return {
        "success": True,
         "planned_plan": {
        "success": True,
        "action": "multi_step",
        "steps": [
            blueprint_plan,
            {
                "success": True,
                "action": "open_app_in_location",
                "app": "vscode",
                "location": f"{location}\\{name}",
                "use_last_created_path": True
            }
        ]
    },
    "project_spec": {
        "custom_features": custom_features,
        "goal": keyword,
        "name": name,
        "template": data["template"],
        "location": location,
        "features": data["features"],
      
    }
}

    return None