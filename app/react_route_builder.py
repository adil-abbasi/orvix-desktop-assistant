import os


def normalize_path(file_path: str):
    return file_path.replace("\\", "/")


def component_name_from_file(file_path):
    file_path = normalize_path(file_path)
    name = os.path.basename(file_path).replace(".jsx", "")

    return "".join(
        part.capitalize()
        for part in name.replace("-", "_").split("_")
        if part.strip()
    )


def route_from_file(file_path, force_home=False):
    file_path = normalize_path(file_path)
    name = os.path.basename(file_path).replace(".jsx", "")

    if force_home or name.lower() == "home":
        return "/"

    return "/" + name.replace("_", "-").replace(" ", "-").lower()


def label_from_component(component):
    label = ""

    for index, char in enumerate(component):
        if index > 0 and char.isupper():
            label += " "
        label += char

    return label.strip()


def build_react_router_files(page_files, app_name="Generated App"):
    if not page_files:
        return {}

    page_files = [normalize_path(path) for path in page_files]

    has_home = any(
        os.path.basename(path).replace(".jsx", "").lower() == "home"
        for path in page_files
    )

    imports = [
        'import { BrowserRouter, Routes, Route, Link } from "react-router-dom";'
    ]

    routes = []
    links = []

    for index, file_path in enumerate(page_files):
        component = component_name_from_file(file_path)

        force_home = False
        if not has_home and index == 0:
            force_home = True

        route = route_from_file(file_path, force_home=force_home)
        label = label_from_component(component)

        imports.append(
            f'import {component} from "./pages/{component}";'
        )

        routes.append(
            f'          <Route path="{route}" element={{<{component} />}} />'
        )

        links.append(
            f'          <Link className="nav-link" to="{route}">{label}</Link>'
        )

    imports_text = "\n".join(imports)
    routes_text = "\n".join(routes)
    links_text = "\n".join(links)

    app_code = f'''{imports_text}

export default function App() {{
  return (
    <BrowserRouter>
      <div className="app-layout">
        <nav className="navbar">
          <div className="brand">{app_name}</div>
          <div className="nav-links">
{links_text}
          </div>
        </nav>

        <Routes>
{routes_text}
        </Routes>
      </div>
    </BrowserRouter>
  );
}}
'''

    return {
        "src/App.jsx": app_code
    }