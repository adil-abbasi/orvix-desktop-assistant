from pathlib import Path


LAST_CREATED_PATH = None
LAST_OPENED_PATH = None
LAST_ACTIVE_PATH = None


def _to_string(path):
    if path is None:
        return None
    return str(path)


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