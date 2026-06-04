import os


def find_react_pages(project_path):
    pages = []

    pages_folder = os.path.join(
        project_path,
        "src",
        "pages"
    )

    if not os.path.exists(pages_folder):
        return pages

    for file in os.listdir(pages_folder):
        if file.endswith(".jsx"):
            pages.append(
                os.path.join(pages_folder, file)
            )

    return pages


def find_key_project_files(project_path):
    possible_files = [
        os.path.join(project_path, "src", "App.jsx"),
        os.path.join(project_path, "src", "main.jsx"),
        os.path.join(project_path, "src", "style.css"),
        os.path.join(project_path, "package.json"),
    ]

    return [
        file_path
        for file_path in possible_files
        if os.path.exists(file_path)
    ]


def read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception:
        return ""


def read_project_files(project_path):
    files = {}

    all_files = []
    all_files.extend(find_key_project_files(project_path))
    all_files.extend(find_react_pages(project_path))

    for file_path in all_files:
        files[file_path] = read_file(file_path)

    return files


def modify_project(project_path, request):
    pages = find_react_pages(project_path)
    project_files = read_project_files(project_path)

    return {
        "success": True,
        "request": request,
        "project_path": project_path,
        "pages_found": len(pages),
        "pages": pages,
        "files_found": len(project_files),
        "project_files": project_files
    }