from pathlib import Path
from rapidfuzz import process

USER_HOME = Path.home()
ONEDRIVE_HOME = USER_HOME / "OneDrive"

BLOCKED_PATHS = [
    Path("C:/Windows"),
    Path("C:/Program Files"),
    Path("C:/Program Files (x86)"),
    Path("C:/ProgramData/Microsoft"),
]

KNOWN_FOLDER_NAMES = {
    "home": "",
    "user": "",
    "desktop": "Desktop",
    "documents": "Documents",
    "downloads": "Downloads",
    "pictures": "Pictures",
    "images": "Pictures",
    "music": "Music",
    "videos": "Videos",
    "onedrive": "OneDrive",
}


def clean_path_text(location: str):
    if not location:
        return "desktop"

    return location.strip().strip('"').strip("'").replace("/", "\\")


def correct_known_location(word: str):
    keys = list(KNOWN_FOLDER_NAMES.keys())
    match = process.extractOne(word.lower().strip(), keys)

    if match and match[1] >= 70:
        return match[0]

    return word.lower().strip()


def get_known_base(key: str):
    key = correct_known_location(key)

    if key in ["home", "user"]:
        return USER_HOME

    if key == "onedrive":
        return ONEDRIVE_HOME

    folder_name = KNOWN_FOLDER_NAMES.get(key)

    if not folder_name:
        return None

    onedrive_path = ONEDRIVE_HOME / folder_name
    normal_path = USER_HOME / folder_name

    # Prefer OneDrive if it exists because your PC uses OneDrive folders
    if onedrive_path.exists():
        return onedrive_path

    if normal_path.exists():
        return normal_path

    return normal_path


def is_drive_path(location: str):
    return len(location) >= 2 and location[1] == ":"


def resolve_location(location: str):
    location = clean_path_text(location)

    if is_drive_path(location):
        return Path(location)

    parts = location.split("\\")
    first = correct_known_location(parts[0])

    base = get_known_base(first)

    if base:
        for part in parts[1:]:
            base = base / part
        return base

    possible_onedrive = ONEDRIVE_HOME / location
    if possible_onedrive.exists():
        return possible_onedrive

    possible_home = USER_HOME / location
    if possible_home.exists():
        return possible_home

    return USER_HOME / location


def normalize_path(path: Path):
    try:
        return path.resolve()
    except Exception:
        return path.absolute()


def is_blocked_path(path: Path):
    path = normalize_path(path)

    for blocked in BLOCKED_PATHS:
        blocked = normalize_path(blocked)
        if path == blocked or blocked in path.parents:
            return True

    dangerous_keywords = [
        "windows",
        "system32",
        "program files",
        "program files (x86)",
        "$recycle.bin",
        "boot",
    ]

    path_text = str(path).lower()

    for keyword in dangerous_keywords:
        if keyword in path_text:
            return True

    return False