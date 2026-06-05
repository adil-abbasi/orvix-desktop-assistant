import json
from app.batch_ai_code_generator import generate_batch_page_files
from app.landing_page_generator import generate_home_page
from app.ui_style_generator import generate_professional_css
from app.react_route_builder import build_react_router_files
from app.project_blueprints import PROJECT_BLUEPRINTS
from app.project_templates import PROJECT_TEMPLATES
from app.feature_composer import compose_feature_files
from app.dynamic_page_generator import generate_dynamic_feature_files
from app.project_memory import save_last_project

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


def normalize_feature_name(name: str):
    return (
        name.lower()
        .replace("&", "")
        .replace("/", " ")
        .replace("-", "_")
        .replace(" ", "_")
        .replace("__", "_")
        .strip("_")
    )


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


def generate_blueprint_project(
    blueprint_name: str,
    project_name: str,
    location: str,
    custom_features=None,
    design_spec=None
):
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

        if design_spec:
            ai_files = generate_batch_page_files(
                project_name,
                design_spec,
                custom_features
            )

            if ai_files:
                files.update(ai_files)

    if design_spec:
        theme = design_spec.get("theme")

    files["src/style.css"] = generate_professional_css(theme)

    page_files = []

    for file_path in files.keys():
        if file_path.startswith("src/pages/") and file_path.endswith(".jsx"):
            page_files.append(file_path)

    if page_files:
        router_files = build_react_router_files(page_files, project_name)
        files.update(router_files)
        files = add_package_dependency(files, "react-router-dom", "latest")
    # actual created path is resolved by file system later; store logical path
    save_last_project(f"{location}\\{project_name}")
    return {
        "success": True,
        "action": "create_project",
        "name": project_name,
        "location": location,
        "template": blueprint["template"],
        "folders": folders,
        "files": files
    }