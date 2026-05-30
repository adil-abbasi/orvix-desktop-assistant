import json
from pathlib import Path


LAST_PROJECT_PATH = None
LAST_PROJECT_TEMPLATE = None

LAST_CREATED_PATH = None
LAST_OPENED_PATH = None
LAST_ACTIVE_PATH = None

PROJECT_MEMORY_FILE = Path("memory/project_memory.json")


def _to_string(path):
    if path is None:
        return None
    return str(path)


def save_project_memory(path, template):
    PROJECT_MEMORY_FILE.parent.mkdir(exist_ok=True)

    with open(PROJECT_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "path": str(path),
                "template": template
            },
            f,
            indent=4
        )


def load_project_memory():
    if not PROJECT_MEMORY_FILE.exists():
        return None, None

    try:
        with open(PROJECT_MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data.get("path"), data.get("template")

    except Exception:
        return None, None


def set_last_project(path, template):
    global LAST_PROJECT_PATH, LAST_PROJECT_TEMPLATE

    LAST_PROJECT_PATH = _to_string(path)
    LAST_PROJECT_TEMPLATE = template

    save_project_memory(path, template)


def get_last_project():
    global LAST_PROJECT_PATH, LAST_PROJECT_TEMPLATE

    if LAST_PROJECT_PATH and LAST_PROJECT_TEMPLATE:
        return LAST_PROJECT_PATH, LAST_PROJECT_TEMPLATE

    path, template = load_project_memory()

    LAST_PROJECT_PATH = path
    LAST_PROJECT_TEMPLATE = template

    return path, template


def set_last_created_path(path):
    global LAST_CREATED_PATH, LAST_ACTIVE_PATH

    LAST_CREATED_PATH = _to_string(path)
    LAST_ACTIVE_PATH = _to_string(path)


def get_last_created_path():
    return LAST_CREATED_PATH


def set_last_opened_path(path):
    global LAST_OPENED_PATH, LAST_ACTIVE_PATH

    LAST_OPENED_PATH = _to_string(path)
    LAST_ACTIVE_PATH = _to_string(path)


def get_last_opened_path():
    return LAST_OPENED_PATH


def set_last_active_path(path):
    global LAST_ACTIVE_PATH

    LAST_ACTIVE_PATH = _to_string(path)


def get_last_active_path():
    return LAST_ACTIVE_PATH


def resolve_reference(value):
    if value is None:
        return value

    text = str(value).strip()
    lower = text.lower()

    reference_words = {
        "it",
        "this",
        "that",
        "last",
        "last one",
        "last created",
        "last opened",
        "created folder",
        "created project",
        "current folder",
        "active folder",
    }

    if lower in reference_words:
        return LAST_ACTIVE_PATH or LAST_CREATED_PATH or LAST_OPENED_PATH or value

    return value