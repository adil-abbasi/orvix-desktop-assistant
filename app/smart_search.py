from pathlib import Path
from rapidfuzz import fuzz

IGNORED_DIRS = {
    ".git", "venv", "__pycache__", "node_modules", ".idea", ".vscode",
    "dist", "build", ".env"
}


def should_ignore(path: Path):
    return any(part in IGNORED_DIRS for part in path.parts)


def find_similar_items(base_path: Path, query: str, item_type: str = "any", limit: int = 10):
    query = query.lower().strip()
    results = []

    if not base_path.exists() or not base_path.is_dir():
        return []

    for path in base_path.rglob("*"):
        if should_ignore(path):
            continue

        if item_type == "file" and not path.is_file():
            continue

        if item_type == "folder" and not path.is_dir():
            continue

        score = fuzz.partial_ratio(query, path.stem.lower())

        if score >= 50:
            results.append({
                "path": path,
                "score": score
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]