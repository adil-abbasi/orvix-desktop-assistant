from app.react_route_builder import build_react_router_files
from app.project_blueprints import PROJECT_BLUEPRINTS
from app.project_templates import PROJECT_TEMPLATES
from app.feature_composer import compose_feature_files
import json


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

def generate_blueprint_project(blueprint_name: str, project_name: str, location: str, custom_features=None):
    blueprint_name = blueprint_name.lower().strip()

    if blueprint_name not in PROJECT_BLUEPRINTS:
        return {
            "success": False,
            "message": f"Unknown blueprint: {blueprint_name}"
        }

    blueprint = PROJECT_BLUEPRINTS[blueprint_name]
    base_template = PROJECT_TEMPLATES[blueprint["template"]]

    folders = list(base_template["folders"])
    files = dict(base_template["files"])

    folders.extend(blueprint.get("folders", []))
    files.update(blueprint.get("files", {}))

    if custom_features:
        files.update(compose_feature_files(custom_features))
        page_files = []

    for file_path in files.keys():
        if file_path.startswith("src/pages/") and file_path.endswith(".jsx"):
            page_files.append(file_path)

    router_files = build_react_router_files(page_files)
    files.update(router_files)
    if page_files:
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
    
    