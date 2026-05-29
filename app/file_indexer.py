from pathlib import Path
import difflib

FILE_INDEX = {}

INDEX_LOCATIONS = [
    Path.home() / "Desktop",
    Path.home() / "OneDrive" / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Downloads",
]

IGNORED_DIRS = {
    ".git",
    "venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode"
}


def should_ignore(path):
    return any(part in IGNORED_DIRS for part in path.parts)


def build_file_index():
    global FILE_INDEX

    FILE_INDEX = {}

    for root in INDEX_LOCATIONS:

        if not root.exists():
            continue

        try:
            for item in root.rglob("*"):

                if should_ignore(item):
                    continue

                if item.is_file():

                    FILE_INDEX[item.name.lower()] = {
                        "name": item.name,
                        "path": str(item),
                        "stem": item.stem.lower(),
                        "suffix": item.suffix.lower()
                    }

        except Exception:
            pass

    return FILE_INDEX


def get_file_index():
    if not FILE_INDEX:
        build_file_index()

    return FILE_INDEX

def find_file(query: str):
    query = query.lower().strip()

    if not FILE_INDEX:
        build_file_index()

    # Exact match
    if query in FILE_INDEX:
        return {
            "found": True,
            "file": FILE_INDEX[query]
        }

    matches = []

    for file_name, file_data in FILE_INDEX.items():

        if query in file_name:
            matches.append(file_data)

    if matches:
        return {
            "found": False,
            "suggestions": matches[:20]
        }

    return {
        "found": False,
        "suggestions": []
    }
def find_file(query: str):

    if not FILE_INDEX:
        build_file_index()

    query = query.lower().strip()

    # Exact filename
    if query in FILE_INDEX:
        return {
            "found": True,
            "file": FILE_INDEX[query]
        }

    # Exact stem
    for file_data in FILE_INDEX.values():
        if file_data["stem"] == query:
            return {
                "found": True,
                "file": file_data
            }

    # Partial match
    partial_matches = []

    for file_data in FILE_INDEX.values():

        if query in file_data["name"].lower():
            partial_matches.append(file_data)

    if partial_matches:
        return {
            "found": False,
            "suggestions": partial_matches[:20]
        }

    # Fuzzy match
    names = [f["name"] for f in FILE_INDEX.values()]

    fuzzy = difflib.get_close_matches(
        query,
        names,
        n=20,
        cutoff=0.45
    )

    if fuzzy:

        suggestions = []

        for name in fuzzy:
            suggestions.append(FILE_INDEX[name.lower()])

        return {
            "found": False,
            "suggestions": suggestions
        }

    return {
        "found": False,
        "suggestions": []
    }