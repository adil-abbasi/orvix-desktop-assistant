from pathlib import Path
from rapidfuzz import fuzz


IGNORED_DIRS = {
    ".git",
    "venv",
    ".venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "coverage",
}


def should_ignore(path: Path):
    try:
        parts = {part.lower() for part in path.parts}
        ignored = {item.lower() for item in IGNORED_DIRS}
        return bool(parts.intersection(ignored))
    except Exception:
        return True


def safe_walk(base_path: Path):
    """
    Safe file/folder scanner.
    Prevents Orvix from crashing on broken OneDrive paths,
    deleted folders, permission errors, and huge folders like node_modules.
    """
    base_path = Path(base_path)

    if not base_path.exists() or not base_path.is_dir():
        return

    stack = [base_path]

    while stack:
        current = stack.pop()

        try:
            if should_ignore(current):
                continue

            if not current.exists():
                continue

            if current.is_dir():
                try:
                    children = list(current.iterdir())
                except (PermissionError, FileNotFoundError, OSError):
                    continue

                for child in children:
                    stack.append(child)
            else:
                yield current

        except (PermissionError, FileNotFoundError, OSError):
            continue


def find_similar_items(base_path: Path, query: str, item_type: str = "any", limit: int = 10):
    query = str(query or "").lower().strip()
    results = []

    base_path = Path(base_path)

    if not query:
        return []

    if not base_path.exists() or not base_path.is_dir():
        return []

    for path in safe_walk(base_path):
        try:
            if should_ignore(path):
                continue

            if item_type == "file" and not path.is_file():
                continue

            if item_type == "folder" and not path.is_dir():
                continue

            name = path.stem.lower()
            full_name = path.name.lower()

            score = fuzz.partial_ratio(query, name)

            if query in name:
                score += 25

            if query in full_name:
                score += 15

            if score >= 50:
                results.append({
                    "path": path,
                    "score": score
                })

        except (PermissionError, FileNotFoundError, OSError):
            continue

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]