import os


def normalize_path(project_path, relative_path):
    relative_path = relative_path.replace("/", os.sep)
    return os.path.join(project_path, relative_path)


def is_safe_project_path(project_path, file_path):
    project_path = os.path.abspath(project_path)
    file_path = os.path.abspath(file_path)

    return file_path.startswith(project_path)


def write_file(project_path, relative_path, content):
    file_path = normalize_path(project_path, relative_path)

    if not is_safe_project_path(project_path, file_path):
        return False, f"Blocked unsafe path: {relative_path}"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return True, f"Updated: {relative_path}"


def apply_file_changes(project_path, changes):
    messages = []

    for relative_path, content in changes.items():
        success, message = write_file(project_path, relative_path, content)
        messages.append(message)

    return {
        "success": True,
        "messages": messages
    }