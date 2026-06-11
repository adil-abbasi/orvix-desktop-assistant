import json
import re
from pathlib import Path


ALLOWED_FILES = {
    "package.json",
    "index.html",
    "src/main.jsx",
    "src/App.jsx",
    "src/styles.css",
}


THEME_PRESETS = {
    "dashboard": {
        "pages": ["Dashboard", "Analytics", "Reports", "Users", "Settings"],
        "style": "premium SaaS analytics dashboard with sidebar, metric cards, charts-looking panels, tables, activity feed"
    },
    "ai tools": {
        "pages": ["Home", "Tools", "Agents", "Pricing", "Docs", "Contact"],
        "style": "futuristic AI tools platform with hero section, glowing cards, agent grid, pricing cards, dark neon layout"
    },
    "saas": {
        "pages": ["Home", "Features", "Solutions", "Pricing", "Testimonials", "Contact"],
        "style": "modern SaaS landing page with gradients, feature cards, split sections, stats, CTA blocks"
    },
    "healthcare": {
        "pages": ["Home", "Services", "Doctors", "Appointments", "Dashboard", "Contact"],
        "style": "clean healthcare platform with medical cards, appointment panel, patient dashboard feel, soft professional layout"
    },
    "ecommerce": {
        "pages": ["Home", "Products", "Categories", "Cart", "Offers", "Contact"],
        "style": "premium ecommerce storefront with product cards, offer banners, category grid, cart preview"
    },
    "finance": {
        "pages": ["Dashboard", "Transactions", "Cards", "Investments", "Reports", "Settings"],
        "style": "fintech banking dashboard with balance cards, spending insights, transaction table, security panels"
    },
    "education": {
        "pages": ["Home", "Courses", "Learning Dashboard", "Assignments", "Progress", "Contact"],
        "style": "online learning platform with course cards, student dashboard, progress bars, assignment panels"
    },
}


def detect_app_type(command: str):
    c = command.lower()

    if "dashboard" in c or "analytics" in c or "admin" in c:
        return "dashboard"

    if "health" in c or "medical" in c or "doctor" in c or "clinic" in c:
        return "healthcare"

    if "ecommerce" in c or "shop" in c or "store" in c:
        return "ecommerce"

    if "finance" in c or "bank" in c or "fintech" in c:
        return "finance"

    if "education" in c or "lms" in c or "course" in c:
        return "education"

    if "saas" in c or "landing" in c:
        return "saas"

    if "ai" in c or "tools" in c or "agent" in c or "neural" in c:
        return "ai tools"

    return "saas"


def detect_visual_theme(command: str):
    c = command.lower()

    if "futuristic" in c or "neon" in c or "cyber" in c:
        return "futuristic dark neon"

    if "premium" in c or "luxury" in c:
        return "premium dark glassmorphism"

    if "minimal" in c or "clean" in c:
        return "minimal clean professional"

    if "colorful" in c:
        return "colorful modern gradient"

    return "premium modern"


def safe_json_extract(text: str):
    if not text:
        return None

    text = text.strip()

    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        return None

    candidate = text[start:end + 1]

    try:
        return json.loads(candidate)
    except Exception:
        return None


def validate_files(data: dict):
    if not isinstance(data, dict):
        return False, "Gemini output is not JSON object."

    files = data.get("files")

    if not isinstance(files, dict):
        return False, "Gemini output missing files object."

    missing = [file for file in ALLOWED_FILES if file not in files]
    if missing:
        return False, f"Gemini output missing files: {missing}"

    for path, content in files.items():
        if path not in ALLOWED_FILES:
            return False, f"Unsafe or unsupported file path from Gemini: {path}"

        if not isinstance(content, str) or not content.strip():
            return False, f"Empty content for file: {path}"

    app = files.get("src/App.jsx", "")
    css = files.get("src/styles.css", "")

    page_count = app.count("const ") + app.count("function ")
    if page_count < 4:
        return False, "App.jsx does not contain enough page/components."

    if "useState" not in app:
        return False, "App.jsx must use navigation state for multiple pages."

    if len(css) < 2500:
        return False, "CSS is too small. Theme likely weak."

    if "background" not in css or "card" not in css.lower():
        return False, "CSS missing real theme styling."

    return True, "valid"


def build_prompt(command: str, project_name: str):
    app_type = detect_app_type(command)
    visual_theme = detect_visual_theme(command)
    preset = THEME_PRESETS[app_type]

    pages = preset["pages"]
    style = preset["style"]

    return f"""
You are an expert senior React frontend engineer and product UI designer.

Create a complete Vite React single page application for this user command:
"{command}"

Project name:
"{project_name}"

App type:
{app_type}

Required visual theme:
{visual_theme}

Required layout direction:
{style}

Required pages:
{", ".join(pages)}

VERY IMPORTANT REQUIREMENTS:
1. Return ONLY valid JSON. No markdown. No explanation.
2. The JSON must have this exact structure:
{{
  "project_type": "react-vite",
  "theme_name": "...",
  "pages": ["..."],
  "files": {{
    "package.json": "...",
    "index.html": "...",
    "src/main.jsx": "...",
    "src/App.jsx": "...",
    "src/styles.css": "..."
  }}
}}
3. src/App.jsx must contain multiple page components.
4. App must have working navigation using React useState.
5. Each page must have a visibly different layout section.
6. Do not generate a simple portfolio.
7. Do not use Tailwind.
8. Do not use external UI libraries.
9. Use only React and CSS.
10. Make the design premium, modern, and presentation-ready.
11. Include realistic dummy data, cards, dashboard panels, feature sections, stats, pricing/contact sections depending on app type.
12. CSS must be detailed and at least 2500 characters.
13. App.jsx must be complete and directly runnable.
14. No placeholder comments like "add more here".
15. No markdown fences.

Make it look like a real startup product website, not a basic template.
"""


def get_local_premium_fallback(project_name: str, command: str):
    app_type = detect_app_type(command)
    visual_theme = detect_visual_theme(command)
    preset = THEME_PRESETS[app_type]

    pages = preset["pages"]

    nav_items = ", ".join([f'"{p}"' for p in pages])

    package_json = """{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "@vitejs/plugin-react": "latest",
    "vite": "latest",
    "react": "latest",
    "react-dom": "latest"
  },
  "devDependencies": {}
}
"""

    index_html = f"""<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_name}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""

    main_jsx = """import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles.css';

createRoot(document.getElementById('root')).render(<App />);
"""

    app_jsx = f"""import React, {{ useState }} from 'react';

const pages = [{nav_items}];

const metrics = [
  {{ label: 'Active users', value: '24.8K', change: '+18%' }},
  {{ label: 'Automation runs', value: '91K', change: '+32%' }},
  {{ label: 'Success rate', value: '98.7%', change: '+4%' }},
  {{ label: 'Saved hours', value: '12.4K', change: '+27%' }}
];

const cards = [
  'AI workflow automation',
  'Smart document generation',
  'Live analytics and insights',
  'Secure team collaboration',
  'No-code command execution',
  'Real-time productivity engine'
];

function Shell({{ active, setActive, children }}) {{
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">O</div>
          <div>
            <h2>{project_name}</h2>
            <p>{app_type.upper()} SYSTEM</p>
          </div>
        </div>

        <nav>
          {{pages.map((page) => (
            <button
              key={{page}}
              className={{active === page ? 'nav-item active' : 'nav-item'}}
              onClick={{() => setActive(page)}}
            >
              {{page}}
            </button>
          ))}}
        </nav>

        <div className="sidebar-card">
          <span>AI Status</span>
          <strong>Online</strong>
          <p>Gemini powered interface generated by Orvix.</p>
        </div>
      </aside>

      <main className="main">
        {{children}}
      </main>
    </div>
  );
}}

function HomePage() {{
  return (
    <>
      <section className="hero">
        <div>
          <span className="eyebrow">Premium React product</span>
          <h1>{project_name} turns ideas into a polished digital experience.</h1>
          <p>
            A modern multi-page interface generated from a natural language command,
            with product sections, live-looking dashboards, and startup-grade design.
          </p>
          <div className="hero-actions">
            <button>Launch workspace</button>
            <button className="secondary">View demo</button>
          </div>
        </div>

        <div className="hero-panel">
          <div className="orb"></div>
          <h3>AI product engine</h3>
          <p>Design system, navigation, cards, analytics, and responsive layouts.</p>
        </div>
      </section>

      <section className="metrics-grid">
        {{metrics.map((item) => (
          <div className="metric-card" key={{item.label}}>
            <span>{{item.label}}</span>
            <strong>{{item.value}}</strong>
            <small>{{item.change}} this month</small>
          </div>
        ))}}
      </section>
    </>
  );
}}

function ToolsPage() {{
  return (
    <section>
      <div className="section-heading">
        <span className="eyebrow">Core modules</span>
        <h2>Everything is structured into clean product blocks.</h2>
      </div>

      <div className="card-grid">
        {{cards.map((card, index) => (
          <div className="feature-card" key={{card}}>
            <span className="card-index">0{{index + 1}}</span>
            <h3>{{card}}</h3>
            <p>
              A production-style component with meaningful content, clear spacing,
              and reusable visual hierarchy.
            </p>
          </div>
        ))}}
      </div>
    </section>
  );
}}

function DashboardPage() {{
  return (
    <section>
      <div className="section-heading">
        <span className="eyebrow">Live overview</span>
        <h2>Command center dashboard</h2>
      </div>

      <div className="dashboard-layout">
        <div className="chart-card large">
          <h3>Performance trend</h3>
          <div className="fake-chart">
            <span style={{{{ height: '45%' }}}}></span>
            <span style={{{{ height: '68%' }}}}></span>
            <span style={{{{ height: '52%' }}}}></span>
            <span style={{{{ height: '78%' }}}}></span>
            <span style={{{{ height: '88%' }}}}></span>
            <span style={{{{ height: '64%' }}}}></span>
            <span style={{{{ height: '92%' }}}}></span>
          </div>
        </div>

        <div className="activity-card">
          <h3>Recent activity</h3>
          {{['Generated React app', 'Created report', 'Built PPT slides', 'Opened VS Code'].map((item) => (
            <div className="activity" key={{item}}>
              <span></span>
              <p>{{item}}</p>
            </div>
          ))}}
        </div>
      </div>
    </section>
  );
}}

function PricingPage() {{
  return (
    <section>
      <div className="section-heading centered">
        <span className="eyebrow">Plans</span>
        <h2>Simple pricing for powerful workflows</h2>
      </div>

      <div className="pricing-grid">
        {{['Starter', 'Pro', 'Enterprise'].map((plan, index) => (
          <div className={{index === 1 ? 'price-card highlighted' : 'price-card'}} key={{plan}}>
            <h3>{{plan}}</h3>
            <strong>${{index === 0 ? '19' : index === 1 ? '49' : '99'}}</strong>
            <p>Perfect for teams that want speed, automation, and polished output.</p>
            <button>{{index === 1 ? 'Start Pro' : 'Choose plan'}}</button>
          </div>
        ))}}
      </div>
    </section>
  );
}}

function ContactPage() {{
  return (
    <section className="contact-section">
      <div>
        <span className="eyebrow">Contact</span>
        <h2>Ready to build your next product interface?</h2>
        <p>
          This page completes the multi-page experience with a real CTA area,
          contact panel, and professional layout.
        </p>
      </div>

      <div className="contact-panel">
        <input placeholder="Your name" />
        <input placeholder="Email address" />
        <textarea placeholder="Tell us about your project"></textarea>
        <button>Send message</button>
      </div>
    </section>
  );
}}

function GenericPage({{ title }}) {{
  if (title === 'Home') return <HomePage />;
  if (['Tools', 'Features', 'Services', 'Solutions', 'Courses', 'Products'].includes(title)) return <ToolsPage />;
  if (['Dashboard', 'Analytics', 'Reports', 'Learning Dashboard'].includes(title)) return <DashboardPage />;
  if (title === 'Pricing') return <PricingPage />;
  if (title === 'Contact') return <ContactPage />;

  return (
    <section>
      <div className="section-heading">
        <span className="eyebrow">{{title}}</span>
        <h2>{{title}} workspace</h2>
      </div>
      <div className="card-grid">
        {{cards.slice(0, 3).map((card) => (
          <div className="feature-card" key={{card}}>
            <h3>{{card}}</h3>
            <p>Custom section generated for the {{title}} page with premium layout.</p>
          </div>
        ))}}
      </div>
    </section>
  );
}}

export default function App() {{
  const [active, setActive] = useState(pages[0]);

  return (
    <Shell active={{active}} setActive={{setActive}}>
      <GenericPage title={{active}} />
    </Shell>
  );
}}
"""

    styles_css = """
:root {
  color-scheme: dark;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #050816;
  color: #f8fafc;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(circle at 15% 10%, rgba(124, 58, 237, 0.28), transparent 32%),
    radial-gradient(circle at 90% 0%, rgba(14, 165, 233, 0.18), transparent 32%),
    linear-gradient(135deg, #050816 0%, #0f172a 55%, #111827 100%);
}

button, input, textarea {
  font: inherit;
}

button {
  cursor: pointer;
  border: 0;
}

.app-shell {
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 100vh;
}

.sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  padding: 28px 20px;
  background: rgba(10, 15, 30, 0.78);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(22px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 34px;
}

.brand-mark {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  display: grid;
  place-items: center;
  color: #030712;
  font-weight: 900;
  background: linear-gradient(135deg, #facc15, #a78bfa, #22d3ee);
  box-shadow: 0 0 30px rgba(167, 139, 250, 0.35);
}

.brand h2 {
  margin: 0;
  font-size: 20px;
}

.brand p {
  margin: 3px 0 0;
  font-size: 11px;
  color: #94a3b8;
  letter-spacing: 0.14em;
}

nav {
  display: grid;
  gap: 10px;
}

.nav-item {
  width: 100%;
  text-align: left;
  padding: 13px 14px;
  border-radius: 14px;
  color: #cbd5e1;
  background: transparent;
  transition: 0.2s ease;
}

.nav-item:hover,
.nav-item.active {
  color: white;
  background: linear-gradient(135deg, rgba(124, 58, 237, 0.36), rgba(14, 165, 233, 0.2));
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.09);
}

.sidebar-card {
  margin-top: 34px;
  padding: 18px;
  border-radius: 20px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
}

.sidebar-card span {
  color: #94a3b8;
  font-size: 13px;
}

.sidebar-card strong {
  display: block;
  margin: 8px 0;
  color: #34d399;
}

.sidebar-card p {
  color: #94a3b8;
  font-size: 13px;
  line-height: 1.6;
}

.main {
  padding: 42px;
}

.hero {
  display: grid;
  grid-template-columns: 1.35fr 0.65fr;
  gap: 28px;
  align-items: stretch;
}

.eyebrow {
  display: inline-flex;
  margin-bottom: 14px;
  color: #facc15;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.hero h1 {
  margin: 0;
  max-width: 850px;
  font-size: clamp(42px, 6vw, 78px);
  line-height: 0.95;
  letter-spacing: -0.06em;
}

.hero p,
.section-heading p,
.contact-section p {
  color: #cbd5e1;
  font-size: 18px;
  line-height: 1.75;
  max-width: 720px;
}

.hero-actions {
  display: flex;
  gap: 14px;
  margin-top: 28px;
}

.hero-actions button,
.price-card button,
.contact-panel button {
  padding: 14px 22px;
  border-radius: 999px;
  color: #030712;
  font-weight: 800;
  background: linear-gradient(135deg, #facc15, #22d3ee);
  box-shadow: 0 18px 50px rgba(34, 211, 238, 0.18);
}

.hero-actions .secondary {
  color: white;
  background: rgba(255,255,255,0.08);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.14);
}

.hero-panel,
.metric-card,
.feature-card,
.chart-card,
.activity-card,
.price-card,
.contact-panel {
  background: linear-gradient(145deg, rgba(255,255,255,0.1), rgba(255,255,255,0.035));
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 28px;
  box-shadow: 0 24px 90px rgba(0,0,0,0.24);
  backdrop-filter: blur(18px);
}

.hero-panel {
  padding: 28px;
  min-height: 360px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  overflow: hidden;
  position: relative;
}

.orb {
  position: absolute;
  width: 190px;
  height: 190px;
  border-radius: 999px;
  top: 36px;
  right: 28px;
  background:
    radial-gradient(circle at 35% 28%, #fff, transparent 9%),
    radial-gradient(circle, #22d3ee 0%, #7c3aed 48%, transparent 70%);
  filter: blur(0.3px);
  box-shadow: 0 0 80px rgba(124, 58, 237, 0.6);
}

.hero-panel h3 {
  margin: 0;
  font-size: 28px;
}

.hero-panel p {
  color: #cbd5e1;
  line-height: 1.7;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-top: 26px;
}

.metric-card {
  padding: 22px;
}

.metric-card span {
  color: #94a3b8;
  font-size: 13px;
}

.metric-card strong {
  display: block;
  margin: 10px 0;
  font-size: 34px;
  letter-spacing: -0.04em;
}

.metric-card small {
  color: #34d399;
}

.section-heading {
  margin-bottom: 28px;
}

.section-heading.centered {
  text-align: center;
}

.section-heading h2,
.contact-section h2 {
  margin: 0;
  font-size: clamp(34px, 4vw, 56px);
  letter-spacing: -0.05em;
  line-height: 1;
}

.card-grid,
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.feature-card,
.price-card {
  padding: 24px;
  min-height: 220px;
}

.card-index {
  color: #facc15;
  font-size: 13px;
  font-weight: 900;
}

.feature-card h3,
.price-card h3,
.chart-card h3,
.activity-card h3 {
  font-size: 24px;
  margin: 14px 0 10px;
}

.feature-card p,
.price-card p {
  color: #cbd5e1;
  line-height: 1.7;
}

.dashboard-layout {
  display: grid;
  grid-template-columns: 1.4fr 0.6fr;
  gap: 20px;
}

.chart-card,
.activity-card {
  padding: 24px;
}

.fake-chart {
  height: 280px;
  display: flex;
  align-items: end;
  gap: 16px;
  padding-top: 24px;
}

.fake-chart span {
  flex: 1;
  border-radius: 16px 16px 4px 4px;
  background: linear-gradient(180deg, #22d3ee, #7c3aed);
  box-shadow: 0 0 34px rgba(34, 211, 238, 0.24);
}

.activity {
  display: flex;
  gap: 12px;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.activity span {
  width: 10px;
  height: 10px;
  border-radius: 99px;
  background: #34d399;
}

.activity p {
  margin: 0;
  color: #cbd5e1;
}

.price-card.highlighted {
  transform: translateY(-10px);
  border-color: rgba(250, 204, 21, 0.45);
  box-shadow: 0 28px 90px rgba(250, 204, 21, 0.12);
}

.price-card strong {
  display: block;
  margin: 12px 0;
  font-size: 48px;
  letter-spacing: -0.05em;
}

.contact-section {
  display: grid;
  grid-template-columns: 1fr 0.85fr;
  gap: 26px;
  align-items: start;
}

.contact-panel {
  display: grid;
  gap: 14px;
  padding: 24px;
}

.contact-panel input,
.contact-panel textarea {
  width: 100%;
  border: 0;
  outline: none;
  color: white;
  padding: 15px 16px;
  border-radius: 16px;
  background: rgba(255,255,255,0.08);
  box-shadow: inset 0 0 0 1px rgba(255,255,255,0.1);
}

.contact-panel textarea {
  min-height: 130px;
  resize: vertical;
}

@media (max-width: 980px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: relative;
    height: auto;
  }

  .hero,
  .dashboard-layout,
  .contact-section {
    grid-template-columns: 1fr;
  }

  .metrics-grid,
  .card-grid,
  .pricing-grid {
    grid-template-columns: 1fr;
  }

  .main {
    padding: 24px;
  }
}
"""

    return {
        "project_type": "react-vite",
        "theme_name": f"{visual_theme} {app_type}",
        "pages": pages,
        "files": {
            "package.json": package_json,
            "index.html": index_html,
            "src/main.jsx": main_jsx,
            "src/App.jsx": app_jsx,
            "src/styles.css": styles_css,
        }
    }


def generate_gemini_react_files(project_name: str, command: str, force_gemini: bool = True):
    prompt = build_prompt(command, project_name)

    if force_gemini:
        try:
            from app.ai.providers import ask_ai

            print("GEMINI REACT BUILDER: Asking Gemini for full multi-page React app...")

            result = ask_ai(prompt, use_cache=False)

            print("GEMINI REACT BUILDER SOURCE:", result.get("source"))

            if result.get("success") and result.get("source") == "gemini":
                data = safe_json_extract(result.get("response", ""))
                valid, reason = validate_files(data)

                if valid:
                    print("GEMINI REACT BUILDER: Gemini app validated.")
                    return data

                print("GEMINI REACT BUILDER: Gemini output rejected:", reason)

            else:
                print("GEMINI REACT BUILDER: Gemini failed or fallback used.")

        except Exception as error:
            print("GEMINI REACT BUILDER ERROR:", error)

    print("GEMINI REACT BUILDER: Using premium local fallback.")
    return get_local_premium_fallback(project_name, command)


def write_react_project(project_path: Path, data: dict):
    files = data.get("files", {})

    for relative_path, content in files.items():
        if relative_path not in ALLOWED_FILES:
            continue

        file_path = project_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

    return True