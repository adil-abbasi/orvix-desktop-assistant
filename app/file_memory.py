import json
from pathlib import Path

MEMORY_FILE = Path("memory/file_memory.json")


def load_memory():
    MEMORY_FILE.parent.mkdir(exist_ok=True)

    if not MEMORY_FILE.exists():
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_memory(data):
    MEMORY_FILE.parent.mkdir(exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def remember_file(alias, path):
    data = load_memory()

    data[alias.lower().strip()] = path

    save_memory(data)


def get_remembered_file(alias):
    data = load_memory()

    return data.get(alias.lower().strip())