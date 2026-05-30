import json

from app.react_route_builder import build_react_router_files
from app.project_blueprints import PROJECT_BLUEPRINTS
from app.project_templates import PROJECT_TEMPLATES
from app.feature_composer import compose_feature_files
from app.dynamic_page_generator import generate_dynamic_feature_files


def add_package_dependency(files, package_name, version="latest"):
    package_json = files.get("package.json")

    if not package_json:
        return files

    data = json.loads(package_json)

    if "dependencies" not in data:
        data["dependencies"] = {}

    data["dependencies"][package_name] = version

    files["package.json"] = json.dumps(data, indent=2)

    return files


def get_blueprint(blueprint_name: str):
    blueprint_name = blueprint_name.lower().strip()

    if blueprint_name in PROJECT_BLUEPRINTS:
        return PROJECT_BLUEPRINTS[blueprint_name]

    return {
        "template": "react app",
        "folders": [
            "src/pages",
            "src/components",
            "src/data"
        ],
        "files": {}
    }


def generate_blueprint_project(blueprint_name: str, project_name: str, location: str, custom_features=None):
    blueprint = get_blueprint(blueprint_name)

    base_template = PROJECT_TEMPLATES[blueprint["template"]]

    folders = list(base_template["folders"])
    files = dict(base_template["files"])

    folders.extend(blueprint.get("folders", []))
    files.update(blueprint.get("files", {}))

    if custom_features:
        dynamic_files = generate_dynamic_feature_files(custom_features)
        registry_files = compose_feature_files(custom_features)

        files.update(dynamic_files)
        files.update(registry_files)

    page_files = []

    for file_path in files.keys():
        if file_path.startswith("src/pages/") and file_path.endswith(".jsx"):
            page_files.append(file_path)

    if page_files:
        router_files = build_react_router_files(page_files)
        files.update(router_files)
        files = add_package_dependency(files, "react-router-dom", "latest")

    return {
        "success": True,
        "action": "create_project",
        "name": project_name,
        "location": location,
        "template": blueprint["template"],
        "folders": folders,
        "files": files
    }