def to_component_name(feature_name: str):
    parts = feature_name.replace("-", "_").split("_")

    return "".join(
        part.capitalize()
        for part in parts
        if part.strip()
    )


def to_title(feature_name: str):
    return feature_name.replace("_", " ").replace("-", " ").title()


def generate_page_code(feature_name: str):
    component_name = to_component_name(feature_name)
    title = to_title(feature_name)

    return f'''function {component_name}() {{
  const items = [
    "{title} Overview",
    "Key Details",
    "Management Section",
    "User Actions"
  ];

  return (
    <section className="page">
      <div className="hero">
        <span className="badge">{title}</span>
        <h1>{title}</h1>
        <p>
          Manage and explore {title.lower()} features from this professional dashboard section.
        </p>
        <button>Explore {title}</button>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Records</h3>
          <div className="stat-value">128</div>
          <p>Active records available in this section.</p>
        </div>

        <div className="stat-card">
          <h3>Pending Tasks</h3>
          <div className="stat-value">24</div>
          <p>Items waiting for review or action.</p>
        </div>

        <div className="stat-card">
          <h3>Completed</h3>
          <div className="stat-value">89%</div>
          <p>Overall completion and activity status.</p>
        </div>
      </div>

      <div className="card-grid">
        {{items.map((item, index) => (
          <div className="card" key={{index}}>
            <h2>{{item}}</h2>
            <p>
              This section is generated dynamically by Orvix based on the requested feature.
            </p>
            <button>View Details</button>
          </div>
        ))}}
      </div>
    </section>
  );
}}

export default {component_name};
'''


def generate_dynamic_feature_files(features):
    files = {}

    for feature in features:
        component_name = to_component_name(feature)

        if not component_name:
            continue

        file_path = f"src/pages/{component_name}.jsx"
        files[file_path] = generate_page_code(feature)

    return files