def component_name_from_file(file_path: str):
    name = file_path.split("/")[-1].replace(".jsx", "")
    return name


def route_path_from_component(component: str):
    if component.lower() == "home":
        return "/"

    route = ""
    for i, char in enumerate(component):
        if char.isupper() and i != 0:
            route += "-"
        route += char.lower()

    return f"/{route}"


def build_react_router_files(page_files: list):
    imports = []
    routes = []
    nav_links = []

    for file_path in page_files:
        component = component_name_from_file(file_path)

        imports.append(f'import {component} from "./pages/{component}";')

        route_path = route_path_from_component(component)
        routes.append(f'        <Route path="{route_path}" element={{<{component} />}} />')

        label = component.replace("Dashboard", " Dashboard")
        nav_links.append(f'      <Link to="{route_path}">{label}</Link>')

    app_jsx = f'''import {{ BrowserRouter, Routes, Route }} from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
{chr(10).join(imports)}
import "./style.css";

function App() {{
  return (
    <BrowserRouter>
      <Navbar />
      <main className="container">
        <Routes>
{chr(10).join(routes)}
        </Routes>
      </main>
      <Footer />
    </BrowserRouter>
  );
}}

export default App;
'''

    navbar_jsx = f'''import {{ Link }} from "react-router-dom";

function Navbar() {{
  return (
    <nav className="navbar">
      <h2>Orvix App</h2>
{chr(10).join(nav_links)}
    </nav>
  );
}}

export default Navbar;
'''

    return {
        "src/App.jsx": app_jsx,
        "src/components/Navbar.jsx": navbar_jsx
    }