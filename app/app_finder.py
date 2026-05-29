from pathlib import Path
import difflib

APP_INDEX = {}


def get_search_locations():
    locations = []

    start_menu_user = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
    start_menu_all = Path("C:/ProgramData/Microsoft/Windows/Start Menu/Programs")
    desktop_user = Path.home() / "Desktop"
    desktop_onedrive = Path.home() / "OneDrive" / "Desktop"

    locations.extend([
        start_menu_user,
        start_menu_all,
        desktop_user,
        desktop_onedrive
    ])

    return locations


def build_app_index():
    global APP_INDEX
    APP_INDEX = {}

    for location in get_search_locations():
        if not location.exists():
            continue

        try:
            for shortcut in location.rglob("*.lnk"):
                name = shortcut.stem.lower().strip()

                if name not in APP_INDEX:
                    APP_INDEX[name] = shortcut

        except Exception:
            pass

    return APP_INDEX


def find_app(app_name):
    if not APP_INDEX:
        build_app_index()

    query = app_name.lower().strip()

    if query in APP_INDEX:
        return {
            "found": True,
            "path": str(APP_INDEX[query]),
            "name": query,
            "suggestions": []
        }

    matches = difflib.get_close_matches(
        query,
        APP_INDEX.keys(),
        n=10,
        cutoff=0.45
    )

    suggestions = []

    for match in matches:
        suggestions.append({
            "name": match,
            "path": str(APP_INDEX[match])
        })

    return {
        "found": False,
        "suggestions": suggestions
    }