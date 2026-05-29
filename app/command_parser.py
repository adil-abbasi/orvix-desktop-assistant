import re
from app.project_templates import PROJECT_TEMPLATES


TEMPLATE_ALIASES = {
    "machine learning project": "ml project",
    "machine learning app": "ml project",
    "ml app": "ml project",
    "ai project": "ml project",

    "frontend app": "react app",
    "frontend project": "react app",
    "react project": "react app",
    "react website": "react app",
    "website": "react app",
    "web app": "react app",

    "backend api": "node express app",
    "api backend": "node express app",
    "express app": "node express app",
    "node app": "node express app",

    "java backend": "spring boot project",
    "spring project": "spring boot project",

    "python project": "python app",
}


FILE_TYPE_EXTENSIONS = {
    "word file": ".docx",
    "document": ".docx",
    "excel file": ".xlsx",
    "spreadsheet": ".xlsx",
    "powerpoint file": ".pptx",
    "presentation": ".pptx",
    "text file": ".txt",
    "python file": ".py",
}


REFERENCE_WORDS = {"it", "this", "that", "last", "last created", "created folder", "created project"}


def is_reference(value: str):
    return value and value.lower().strip() in REFERENCE_WORDS


def split_commands(command: str):
    command = command.strip()
    lower = command.lower()

    special_endings = [
        (" and open it in vscode", "open it in vscode"),
        (" and open it in vs code", "open it in vscode"),
        (" and open it in visual studio code", "open it in vscode"),
        (" and run it", "run it"),
        (" and open it", "open it"),
    ]

    project_starters = [
        "create project",
        "create ml project",
        "create data science project",
        "create flask app",
        "create python app",
        "create react app",
        "create django app",
        "create node express app",
        "create spring boot project",
        "create machine learning project",
        "create ml app",
        "create ai project",
        "create frontend app",
        "create website",
        "create web app",
        "create backend api",
        "create api backend",
        "create express app",
        "create java backend",
        "create spring project",
        "create python project",
        "create react project",
    ]

    for starter in project_starters:
        if lower.startswith(starter):
            for ending, action in special_endings:
                if lower.endswith(ending):
                    return [command[:-len(ending)].strip(), action]
            return [command]

    parts = re.split(r"\s+(?:and then|then|and)\s+", command, flags=re.IGNORECASE)
    return [p.strip() for p in parts if p.strip()]


def normalize_connectors(text: str):
    return (
        text.strip()
        .replace(" from ", " in ")
        .replace(" inside ", " in ")
        .replace(" at ", " in ")
        .replace(" on ", " in ")
    )


def extract_name_and_location(text: str):
    text = normalize_connectors(text)
    match = re.match(r"(.+?)\s+in\s+(.+)", text, flags=re.IGNORECASE)

    if match:
        return match.group(1).strip(), match.group(2).strip()

    return text.strip(), "desktop"


def normalize_file_creation_text(text: str):
    lower = text.lower().strip()

    for file_type, extension in FILE_TYPE_EXTENSIONS.items():
        if lower.startswith(file_type):
            remaining = text[len(file_type):].strip()
            remaining = re.sub(r"^(named|called|name)\s+", "", remaining, flags=re.IGNORECASE).strip()

            if not remaining.lower().endswith(extension):
                remaining += extension

            return remaining

    return re.sub(r"^(named|called|name)\s+", "", text, flags=re.IGNORECASE).strip()


def parse_create_project(command: str):
    pattern = r"create\s+project\s+(.+?)\s+(?:in|on|at|inside)\s+(.+?)\s+with\s+folders\s+(.+?)\s+and\s+files\s+(.+)"
    match = re.match(pattern, command, flags=re.IGNORECASE)

    if not match:
        return {
            "success": False,
            "message": "Invalid project format. Use: create project MLProject in desktop with folders src, data and files main.py, README.md"
        }

    folders = [f.strip() for f in match.group(3).split(",") if f.strip()]
    files = [f.strip() for f in match.group(4).split(",") if f.strip()]

    return {
        "success": True,
        "action": "create_project",
        "name": match.group(1).strip(),
        "location": match.group(2).strip(),
        "folders": folders,
        "files": files
    }


def parse_template_project(command: str):
    pattern = r"create\s+(.+?)\s+([A-Za-z0-9_\-]+)\s+(?:in|on|at|inside)\s+(.+)"
    match = re.match(pattern, command, flags=re.IGNORECASE)

    if not match:
        return None

    template_name = match.group(1).lower().strip()
    project_name = match.group(2).strip()
    location = match.group(3).strip()

    template_name = TEMPLATE_ALIASES.get(template_name, template_name)

    if template_name not in PROJECT_TEMPLATES:
        return None

    template = PROJECT_TEMPLATES[template_name]

    return {
        "success": True,
        "action": "create_project",
        "name": project_name,
        "location": location,
        "template": template_name,
        "folders": template["folders"],
        "files": template["files"]
    }


def parse_run_project(command: str):
    lower = command.lower().strip()

    if lower == "run it":
        return {
            "success": True,
            "action": "run_project",
            "template": "react app",
            "name": "",
            "location": "it"
        }

    pattern = r"run\s+(.+?)\s+([A-Za-z0-9_\-]+)\s+(?:from|in|at|inside|on)\s+(.+)"
    match = re.match(pattern, command, flags=re.IGNORECASE)

    if not match:
        return None

    template_name = match.group(1).lower().strip()
    project_name = match.group(2).strip()
    location = match.group(3).strip()

    template_name = TEMPLATE_ALIASES.get(template_name, template_name)

    return {
        "success": True,
        "action": "run_project",
        "template": template_name,
        "name": project_name,
        "location": location
    }


def parse_copy_move(command: str, operation: str):
    pattern = rf"{operation}\s+(file|folder)\s+(.+?)\s+from\s+(.+?)\s+to\s+(.+)"
    match = re.match(pattern, command, flags=re.IGNORECASE)

    if not match:
        return {"success": False, "message": f"Invalid {operation} command format."}

    return {
        "success": True,
        "action": operation,
        "item_type": match.group(1).lower().strip(),
        "name": match.group(2).strip(),
        "source": match.group(3).strip(),
        "destination": match.group(4).strip()
    }


def parse_rename(command: str):
    pattern = r"rename\s+(file|folder)\s+(.+?)\s+to\s+(.+?)\s+(?:in|inside|at|from|on)\s+(.+)"
    match = re.match(pattern, command, flags=re.IGNORECASE)

    if not match:
        return {"success": False, "message": "Invalid rename format."}

    return {
        "success": True,
        "action": "rename",
        "item_type": match.group(1).lower().strip(),
        "old_name": match.group(2).strip(),
        "new_name": match.group(3).strip(),
        "location": match.group(4).strip()
    }


def parse_delete(command: str):
    lower = command.lower().strip()

    if lower in ["delete it", "remove it", "delete this", "remove this"]:
        return {
            "success": True,
            "action": "delete",
            "item_type": "folder",
            "name": "",
            "location": "it",
            "requires_confirmation": True
        }

    pattern = r"delete\s+(file|folder)\s+(.+?)\s+(?:from|in|inside|at|on)\s+(.+)"
    match = re.match(pattern, command, flags=re.IGNORECASE)

    if not match:
        return {"success": False, "message": "Invalid delete format."}

    return {
        "success": True,
        "action": "delete",
        "item_type": match.group(1).lower().strip(),
        "name": match.group(2).strip(),
        "location": match.group(3).strip(),
        "requires_confirmation": True
    }


def parse_open_folder(command: str):
    lower = command.lower().strip()

    if lower in ["open it", "open this", "open that", "open last"]:
        return {
            "success": True,
            "action": "open_folder",
            "name": "",
            "location": "it"
        }

    patterns = [
        r"open\s+folder\s+(.+?)\s+(?:from|in|inside|at|on)\s+(.+)",
        r"open\s+(.+?)\s+folder\s+(?:from|in|inside|at|on)\s+(.+)",
    ]

    for pattern in patterns:
        match = re.match(pattern, command, flags=re.IGNORECASE)
        if match:
            return {
                "success": True,
                "action": "open_folder",
                "name": match.group(1).strip(),
                "location": match.group(2).strip()
            }

    simple_match = re.match(r"open\s+folder\s+(.+)", command, flags=re.IGNORECASE)
    if simple_match:
        return {
            "success": True,
            "action": "open_folder",
            "name": "",
            "location": simple_match.group(1).strip()
        }

    return {"success": False, "message": "Invalid open folder format."}


def parse_open_file(command: str):
    pattern = r"open\s+(?:file\s+)?(.+?)\s+(?:from|in|inside|at|on)\s+(.+)"
    match = re.match(pattern, command, flags=re.IGNORECASE)

    if not match:
        return {"success": False, "message": "Invalid open file format."}

    return {
        "success": True,
        "action": "open_file",
        "name": match.group(1).strip(),
        "location": match.group(2).strip()
    }


def parse_open_app_in_location(command: str):
    lower = command.lower().strip()

    if lower in [
        "open it in vscode",
        "open it in vs code",
        "open it in visual studio code",
        "open this in vscode",
        "open that in vscode",
    ]:
        return {
            "success": True,
            "action": "open_app_in_location",
            "app": "vscode",
            "location": "it",
            "use_last_created_path": True
        }

    vscode_match = re.match(
        r"open\s+(?:vscode|vs code|visual studio code)\s+(?:in|at|inside|from)\s+(.+)",
        command,
        flags=re.IGNORECASE
    )

    if vscode_match:
        return {
            "success": True,
            "action": "open_app_in_location",
            "app": "vscode",
            "location": vscode_match.group(1).strip()
        }

    return None


def parse_list_folder(command: str):
    lower = command.lower().strip()

    if lower in ["list it", "show it", "show files in it", "list files in it"]:
        return {
            "success": True,
            "action": "list_folder",
            "location": "it"
        }

    pattern = r"list\s+(?:folder\s+)?(.+)"
    match = re.match(pattern, command, flags=re.IGNORECASE)

    if not match:
        return {"success": False, "message": "Invalid list format."}

    return {
        "success": True,
        "action": "list_folder",
        "location": match.group(1).strip()
    }


def parse_search_file(command: str):
    pattern = r"search\s+(?:file\s+)?(.+?)\s+(?:in|inside|at|from|on)\s+(.+)"
    match = re.match(pattern, command, flags=re.IGNORECASE)

    if not match:
        return {"success": False, "message": "Invalid search format."}

    return {
        "success": True,
        "action": "search_file",
        "query": match.group(1).strip(),
        "location": match.group(2).strip()
    }


def parse_create_folder(command: str):
    if command.lower().startswith("create a folder"):
        remaining = command[len("create a folder"):].strip()
    else:
        remaining = command[len("create folder"):].strip()

    name, location = extract_name_and_location(remaining)

    if not name:
        return {"success": False, "message": "Folder name missing."}

    return {
        "success": True,
        "action": "create_folder",
        "name": name,
        "location": location
    }


def parse_create_file(command: str):
    lower = command.lower()

    prefixes = [
        "create file ",
        "create word file ",
        "create excel file ",
        "create powerpoint file ",
        "create text file ",
        "create python file ",
        "create document ",
        "create spreadsheet ",
        "create presentation ",
        "create a ",
    ]

    remaining = None

    for prefix in prefixes:
        if lower.startswith(prefix):
            if prefix == "create a ":
                remaining = command[len("create a "):].strip()
            elif prefix == "create file ":
                remaining = command[len("create file "):].strip()
            else:
                file_type = prefix.replace("create ", "").strip()
                rest = command[len(prefix):].strip()
                remaining = f"{file_type} {rest}"
            break

    if remaining is None:
        return {"success": False, "message": "Invalid create file command."}

    name, location = extract_name_and_location(remaining)
    name = normalize_file_creation_text(name)

    if not name:
        return {"success": False, "message": "File name missing."}

    return {
        "success": True,
        "action": "create_file",
        "name": name,
        "location": location
    }


def parse_single_command(command: str):
    command = command.strip()
    lower = command.lower()

    app_location = parse_open_app_in_location(command)
    if app_location:
        return app_location

    run_project = parse_run_project(command)
    if run_project:
        return run_project

    template_project = parse_template_project(command)
    if template_project:
        return template_project

    if lower.startswith("create project"):
        return parse_create_project(command)

    if lower.startswith("copy "):
        return parse_copy_move(command, "copy")

    if lower.startswith("move ") or lower.startswith("cut "):
        normalized = re.sub(r"^cut\s+", "move ", command, flags=re.IGNORECASE)
        return parse_copy_move(normalized, "move")

    if lower.startswith("rename "):
        return parse_rename(command)

    if lower.startswith("delete ") or lower.startswith("remove "):
        normalized = re.sub(r"^remove\s+", "delete ", command, flags=re.IGNORECASE)
        return parse_delete(normalized)

    if lower.startswith("list ") or lower in ["show it", "show files in it"]:
        return parse_list_folder(command)

    if lower.startswith("search "):
        return parse_search_file(command)

    if lower.startswith("create a folder") or lower.startswith("create folder"):
        return parse_create_folder(command)

    if (
        lower.startswith("create file")
        or lower.startswith("create a ")
        or lower.startswith("create word file")
        or lower.startswith("create excel file")
        or lower.startswith("create powerpoint file")
        or lower.startswith("create text file")
        or lower.startswith("create python file")
        or lower.startswith("create document")
        or lower.startswith("create spreadsheet")
        or lower.startswith("create presentation")
    ):
        return parse_create_file(command)

    if lower.startswith("open folder") or lower in ["open it", "open this", "open that", "open last"] or re.match(r"open\s+.+?\s+folder\s+(from|in|inside|at|on)\s+.+", lower):
        return parse_open_folder(command)

    if lower.startswith("open app"):
        app_name = command[len("open app"):].strip()
        return {"success": True, "action": "open_app", "app": app_name}

    if lower.startswith("open "):
        if re.search(r"\s+(from|in|inside|at|on)\s+", lower):
            return parse_open_file(command)

        target = command[len("open "):].strip()

        known_apps = [
            "vscode", "vs code", "visual studio code",
            "chrome", "google chrome", "notepad",
            "calculator", "paint", "cmd", "terminal",
            "file explorer", "word", "excel", "powerpoint",
            "telegram", "localsend", "local send",
            "pycharm", "android studio", "mysql workbench"
        ]

        if target.lower() in known_apps:
            return {
                "success": True,
                "action": "open_app",
                "app": target
            }

        return {
            "success": True,
            "action": "smart_open_file",
            "query": target
        }

    return {"success": False, "message": f"Command not recognized yet: {command}"}


def parse_command(command: str):
    commands = split_commands(command)
    parsed_steps = []

    for cmd in commands:
        parsed = parse_single_command(cmd)

        if not parsed["success"]:
            return parsed

        parsed_steps.append(parsed)

    if len(parsed_steps) == 1:
        return parsed_steps[0]

    return {
        "success": True,
        "action": "multi_step",
        "steps": parsed_steps
    }