import json
import os

MEMORY_FILE = os.path.join("memory", "word_memory.json")


def ensure_memory_folder():
    os.makedirs("memory", exist_ok=True)


def save_current_document(path):
    ensure_memory_folder()

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"current_document": os.path.abspath(path)},
            file,
            indent=2
        )


def load_current_document():
    if not os.path.exists(MEMORY_FILE):
        return None

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        path = data.get("current_document")

        if path and os.path.exists(path):
            return path

        return None

    except Exception:
        return None
    