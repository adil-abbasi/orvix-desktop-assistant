def normalize_feature(feature_name: str):
    return (
        str(feature_name)
        .lower()
        .replace("&", "and")
        .replace("/", "_")
        .replace("-", "_")
        .replace(" ", "_")
        .replace("__", "_")
        .strip("_")
    )


def to_component_name(feature_name: str):
    feature_name = normalize_feature(feature_name)
    parts = feature_name.split("_")

    component = "".join(
        part.capitalize()
        for part in parts
        if part.strip()
    )

    return component or "Page"


def to_title(feature_name: str):
    feature_name = normalize_feature(feature_name)

    return (
        feature_name
        .replace("_", " ")
        .title()
    )


def detect_page_type(feature_name: str):
    feature = normalize_feature(feature_name)

    if feature in ["home", "landing", "landing_page"]:
        return "home"

    if feature in ["about", "profile"]:
        return "about"

    if feature in ["projects", "portfolio", "work"]:
        return "projects"

    if feature in ["skills", "technologies", "tools"]:
        return "skills"

    if feature in ["services", "solutions"]:
        return "services"

    if feature in ["contact", "connect"]:
        return "contact"

    if feature in ["dashboard", "analytics", "admin"]:
        return "dashboard"

    return "general"


def generate_home_page(component_name: str, title: str):
    return f'''import React from "react";

export default function {component_name}() {{
  const highlights = [
    "Premium responsive interface",
    "Clean section-based layout",
    "Modern user experience"
  ];

  return (
    <main className="page">
      <section className="hero-section premium-hero">
        <p className="eyebrow">Premium Portfolio</p>
        <h1>Build a strong digital presence with a modern portfolio.</h1>
        <p>
          This website is designed to present skills, projects, services, and
          contact information in a clean, professional, and impressive way.
        </p>

        <div className="hero-actions">
          <a className="primary-btn" href="/projects">View Projects</a>
          <a className="secondary-btn" href="/contact">Contact Me</a>
        </div>
      </section>

      <section className="content-grid">
        {{highlights.map((item, index) => (
          <div className="card" key={{index}}>
            <span className="card-number">0{{index + 1}}</span>
            <h2>{{item}}</h2>
            <p>
              Orvix generated this section with a structured layout so the
              project looks complete, useful, and ready for further editing.
            </p>
          </div>
        ))}}
      </section>

      <section className="highlight-section">
        <h2>Designed for real presentation</h2>
        <p>
          The layout uses reusable sections, professional spacing, and clean
          routing so the project does not feel like an empty starter template.
        </p>
      </section>
    </main>
  );
}}
'''


def generate_about_page(component_name: str, title: str):
    return f'''import React from "react";

export default function {component_name}() {{
  const values = [
    "Problem solving",
    "Clean design",
    "Practical development",
    "Continuous learning"
  ];

  return (
    <main className="page">
      <section className="hero-section">
        <p className="eyebrow">{title}</p>
        <h1>A focused profile built around skills, projects, and growth.</h1>
        <p>
          This section introduces the person, brand, or platform behind the
          portfolio. It explains the purpose, background, and professional value.
        </p>
      </section>

      <section className="content-grid">
        {{values.map((value, index) => (
          <div className="card" key={{index}}>
            <h2>{{value}}</h2>
            <p>
              This value helps define the quality and direction of the work
              presented across the portfolio.
            </p>
          </div>
        ))}}
      </section>

      <section className="highlight-section">
        <h2>About this portfolio</h2>
        <p>
          It is structured to communicate capability clearly through experience,
          skills, projects, and contact sections.
        </p>
      </section>
    </main>
  );
}}
'''


def generate_projects_page(component_name: str, title: str):
    return f'''import React from "react";

export default function {component_name}() {{
  const projects = [
    "AI Desktop Assistant",
    "Data Science Dashboard",
    "Machine Learning Predictor",
    "Modern Web Application"
  ];

  return (
    <main className="page">
      <section className="hero-section">
        <p className="eyebrow">{title}</p>
        <h1>Selected projects with practical impact and clean execution.</h1>
        <p>
          This section highlights important work, project goals, technology
          choices, and the value created through each solution.
        </p>
      </section>

      <section className="content-grid">
        {{projects.map((project, index) => (
          <div className="card project-card" key={{index}}>
            <span className="card-number">0{{index + 1}}</span>
            <h2>{{project}}</h2>
            <p>
              A structured project card that can be expanded with real features,
              screenshots, GitHub links, and live demo information.
            </p>
            <a className="text-link" href="#">View case study</a>
          </div>
        ))}}
      </section>
    </main>
  );
}}
'''


def generate_skills_page(component_name: str, title: str):
    return f'''import React from "react";

export default function {component_name}() {{
  const skills = [
    "Python",
    "React",
    "Machine Learning",
    "SQL",
    "Data Visualization",
    "Automation"
  ];

  return (
    <main className="page">
      <section className="hero-section">
        <p className="eyebrow">{title}</p>
        <h1>Technical skills organized for a strong professional impression.</h1>
        <p>
          This section presents tools, technologies, and practical abilities in
          a clear and easy-to-understand format.
        </p>
      </section>

      <section className="skill-cloud">
        {{skills.map((skill, index) => (
          <span className="skill-pill" key={{index}}>{{skill}}</span>
        ))}}
      </section>

      <section className="content-grid">
        <div className="card">
          <h2>Development</h2>
          <p>Building clean interfaces, structured projects, and useful tools.</p>
        </div>

        <div className="card">
          <h2>Data Science</h2>
          <p>Working with data cleaning, prediction models, and visualization.</p>
        </div>

        <div className="card">
          <h2>Automation</h2>
          <p>Creating smart workflows that reduce manual effort and save time.</p>
        </div>
      </section>
    </main>
  );
}}
'''


def generate_services_page(component_name: str, title: str):
    return f'''import React from "react";

export default function {component_name}() {{
  const services = [
    "Web development",
    "AI automation",
    "Data analysis",
    "Dashboard design"
  ];

  return (
    <main className="page">
      <section className="hero-section">
        <p className="eyebrow">{title}</p>
        <h1>Services designed to solve real digital problems.</h1>
        <p>
          This page explains the main services, solutions, or features offered
          by the platform in a clean and professional way.
        </p>
      </section>

      <section className="content-grid">
        {{services.map((service, index) => (
          <div className="card" key={{index}}>
            <span className="card-number">0{{index + 1}}</span>
            <h2>{{service}}</h2>
            <p>
              A professional service section with clear value, practical use
              cases, and room for future details.
            </p>
          </div>
        ))}}
      </section>
    </main>
  );
}}
'''


def generate_contact_page(component_name: str, title: str):
    return f'''import React from "react";

export default function {component_name}() {{
  return (
    <main className="page">
      <section className="hero-section">
        <p className="eyebrow">{title}</p>
        <h1>Let’s connect and build something useful.</h1>
        <p>
          This contact section gives visitors a simple way to reach out for
          projects, collaboration, internships, or professional opportunities.
        </p>
      </section>

      <section className="highlight-section contact-panel">
        <h2>Contact Information</h2>
        <p>Email: your.email@example.com</p>
        <p>LinkedIn: linkedin.com/in/your-profile</p>
        <p>Location: Karachi, Pakistan</p>
        <a className="primary-btn" href="mailto:your.email@example.com">
          Send Email
        </a>
      </section>
    </main>
  );
}}
'''


def generate_dashboard_page(component_name: str, title: str):
    return f'''import React from "react";

export default function {component_name}() {{
  const stats = [
    {{ label: "Total Records", value: "128" }},
    {{ label: "Pending Tasks", value: "24" }},
    {{ label: "Completed", value: "89%" }}
  ];

  return (
    <main className="page">
      <section className="hero-section">
        <p className="eyebrow">{title}</p>
        <h1>Professional dashboard section for managing key activity.</h1>
        <p>
          Track information, review important metrics, and manage workflow from
          a clean dashboard-style page.
        </p>
      </section>

      <section className="content-grid">
        {{stats.map((stat, index) => (
          <div className="card stat-card" key={{index}}>
            <p className="eyebrow">{{stat.label}}</p>
            <h2>{{stat.value}}</h2>
            <p>Live-ready metric card generated by Orvix.</p>
          </div>
        ))}}
      </section>
    </main>
  );
}}
'''


def generate_general_page(component_name: str, title: str):
    return f'''import React from "react";

export default function {component_name}() {{
  const sections = [
    "Overview",
    "Key Benefits",
    "Practical Use",
    "Next Step"
  ];

  return (
    <main className="page">
      <section className="hero-section">
        <p className="eyebrow">{title}</p>
        <h1>{title} built with a clean, professional layout.</h1>
        <p>
          This page was generated dynamically by Orvix and can be expanded with
          real data, forms, dashboards, or backend API integration.
        </p>
      </section>

      <section className="content-grid">
        {{sections.map((section, index) => (
          <div className="card" key={{index}}>
            <span className="card-number">0{{index + 1}}</span>
            <h2>{{section}}</h2>
            <p>
              This section gives structure to the page and keeps the project
              useful even when AI generation is unavailable.
            </p>
          </div>
        ))}}
      </section>
    </main>
  );
}}
'''


def generate_page_code(feature_name: str):
    component_name = to_component_name(feature_name)
    title = to_title(feature_name)
    page_type = detect_page_type(feature_name)

    if page_type == "home":
        return generate_home_page(component_name, title)

    if page_type == "about":
        return generate_about_page(component_name, title)

    if page_type == "projects":
        return generate_projects_page(component_name, title)

    if page_type == "skills":
        return generate_skills_page(component_name, title)

    if page_type == "services":
        return generate_services_page(component_name, title)

    if page_type == "contact":
        return generate_contact_page(component_name, title)

    if page_type == "dashboard":
        return generate_dashboard_page(component_name, title)

    return generate_general_page(component_name, title)


def generate_dynamic_feature_files(features):
    files = {}

    for feature in features:
        component_name = to_component_name(feature)

        if not component_name:
            continue

        file_path = f"src/pages/{component_name}.jsx"
        files[file_path] = generate_page_code(feature)

    return files