import os


def component_name_from_file(file_path):
    name = os.path.basename(file_path).replace(".jsx", "")

    return "".join(
        part.capitalize()
        for part in name.replace("-", "_").split("_")
        if part.strip()
    )


def route_from_file(file_path):
    name = os.path.basename(file_path).replace(".jsx", "")

    if name.lower() == "home":
        return "/"

    return "/" + name.replace("_", "-").lower()


def build_react_router_files(page_files, app_name="Generated App"):
    imports = [
        'import { BrowserRouter, Routes, Route, Link } from "react-router-dom";'
    ]

    routes = []
    links = []

    for file_path in page_files:
        component = component_name_from_file(file_path)
        route = route_from_file(file_path)

        imports.append(
            f'import {component} from "./pages/{component}";'
        )

        routes.append(
            f'          <Route path="{route}" element={{<{component} />}} />'
        )

        links.append(
            f'          <Link to="{route}">{component}</Link>'
        )

    imports_text = "\n".join(imports)
    routes_text = "\n".join(routes)
    links_text = "\n".join(links)

    app_code = f'''{imports_text}

function App() {{
  return (
    <BrowserRouter>
      <nav className="navbar">
        <h2>{app_name}</h2>
{links_text}
      </nav>

      <main className="container">
        <Routes>
{routes_text}
        </Routes>
      </main>
    </BrowserRouter>
  );
}}

export default App;
'''

    return {
        "src/App.jsx": app_code
    }