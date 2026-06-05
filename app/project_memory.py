import json
import os

MEMORY_FILE = os.path.join("memory", "project_memory.json")


def ensure_memory_folder():
    os.makedirs("memory", exist_ok=True)


def save_last_project(path):
    ensure_memory_folder()

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"last_project_path": path},
            file,
            indent=2
        )


def load_last_project():
    if not os.path.exists(MEMORY_FILE):
        return None

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data.get("last_project_path")
    except Exception:
        return None