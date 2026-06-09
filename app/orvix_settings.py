import json
import os

SETTINGS_PATH = os.path.join("memory", "settings.json")

DEFAULT_SETTINGS = {
    "writing_mode": "demo"
}


def save_settings(settings):
    os.makedirs("memory", exist_ok=True)

    with open(SETTINGS_PATH, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def ensure_settings():
    os.makedirs("memory", exist_ok=True)

    if not os.path.exists(SETTINGS_PATH):
        save_settings(DEFAULT_SETTINGS)
        return

    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            save_settings(DEFAULT_SETTINGS)
            return

        json.loads(content)

    except Exception:
        save_settings(DEFAULT_SETTINGS)


def load_settings():
    ensure_settings()

    with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def get_writing_mode():
    settings = load_settings()
    return settings.get("writing_mode", "demo")


def set_writing_mode(mode):
    allowed = ["instant", "fast", "moderate", "typewriter", "demo"]

    if mode not in allowed:
        mode = "demo"

    settings = load_settings()
    settings["writing_mode"] = mode
    save_settings(settings)