import json
import re

from app.ai.providers import ask_ai


DOMAIN_DEFAULT_PAGES = {
    "school": ["home", "about", "admissions", "classes", "teachers", "events", "contact"],
    "hospital": ["home", "departments", "doctors", "appointment", "services", "contact"],
    "restaurant": ["home", "menu", "chefs", "reservation", "gallery", "reviews", "contact"],
    "ecommerce": ["home", "products", "categories", "offers", "cart", "contact"],
    "real_estate": ["home", "properties", "agents", "pricing", "gallery", "contact"],
    "gym": ["home", "programs", "trainers", "pricing", "schedule", "contact"],
    "travel": ["home", "destinations", "packages", "hotels", "booking", "contact"],
    "finance": ["home", "dashboard", "transactions", "cards", "investments", "contact"],
    "ai_tools": ["home", "tools", "agents", "pricing", "docs", "contact"],
    "saas": ["home", "features", "solutions", "pricing", "testimonials", "contact"],
    "portfolio": ["home", "about", "projects", "skills", "services", "contact"],
    "car_showroom": ["home", "cars", "services", "financing", "gallery", "contact"],
    "general": ["home", "about", "services", "portfolio", "pricing", "contact"],
}


def extract_json(text: str):
    """
    Extract files from Gemini response.
    Supports:
    1. JSON object
    2. {"files": {...}}
    3. FILE_START / FILE_END blocks
    """

    if not text:
        print("REACT EXTRACTOR: Empty response.")
        return None

    text = str(text).strip()

    # Debug preview
    print("REACT EXTRACTOR PREVIEW:", text[:500].replace("\n", " ")[:500])

    # Remove markdown fences if pure JSON
    cleaned = text.strip()
    cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^```\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    # Try direct JSON
    try:
        data = json.loads(cleaned)

        if isinstance(data, dict) and isinstance(data.get("files"), dict):
            return data["files"]

        if isinstance(data, dict):
            return data

    except Exception:
        pass

    # Try JSON object inside text
    match = re.search(r"\{[\s\S]*\}", cleaned)

    if match:
        try:
            data = json.loads(match.group(0))

            if isinstance(data, dict) and isinstance(data.get("files"), dict):
                return data["files"]

            if isinstance(data, dict):
                return data

        except Exception:
            pass

    # Try FILE_START / FILE_END block format
    files = {}

    block_pattern = re.compile(
        r"FILE_START:\s*(.*?)\s*\n([\s\S]*?)\nFILE_END",
        re.IGNORECASE
    )

    for match in block_pattern.finditer(text):
        path = match.group(1).strip()
        content = match.group(2).strip()

        # Remove accidental code fences inside file block
        content = re.sub(r"^```jsx\s*", "", content, flags=re.IGNORECASE)
        content = re.sub(r"^```javascript\s*", "", content, flags=re.IGNORECASE)
        content = re.sub(r"^```\s*", "", content)
        content = re.sub(r"\s*```$", "", content)

        if path and content:
            files[path] = content

    if files:
        print("REACT EXTRACTOR: Parsed FILE_START blocks:", list(files.keys()))
        return files

    print("REACT EXTRACTOR: Could not parse Gemini response.")
    return None

def normalize_feature(feature: str):
    return (
        str(feature)
        .lower()
        .replace("&", "and")
        .replace("/", "_")
        .replace("-", "_")
        .replace(" ", "_")
        .replace("__", "_")
        .strip("_")
    )


def feature_to_component(feature: str):
    feature = normalize_feature(feature)
    parts = feature.split("_")

    component = "".join(
        part.capitalize()
        for part in parts
        if part.strip()
    )

    return component or "Page"


def feature_to_title(feature: str):
    feature = normalize_feature(feature)

    return feature.replace("_", " ").title()


def detect_website_type(project_name, design_spec, features):
    text = f"{project_name} {design_spec} {' '.join(features or [])}".lower()

    checks = {
        "school": ["school", "academy", "college", "university", "education", "classes", "admission", "teacher"],
        "hospital": ["hospital", "clinic", "doctor", "medical", "healthcare", "patient", "appointment", "department"],
        "restaurant": ["restaurant", "food", "cafe", "menu", "chef", "reservation"],
        "ecommerce": ["ecommerce", "shop", "store", "products", "cart", "marketplace"],
        "real_estate": ["real estate", "property", "apartment", "homes", "rent", "sale"],
        "gym": ["gym", "fitness", "workout", "trainer"],
        "travel": ["travel", "tour", "hotel", "booking", "destination"],
        "finance": ["finance", "bank", "fintech", "wallet", "investment", "transaction"],
        "ai_tools": ["ai", "tools", "agents", "neural", "automation"],
        "saas": ["saas", "startup", "software", "platform"],
        "portfolio": ["portfolio", "resume", "personal website"],
        "car_showroom": ["car", "showroom", "automobile", "vehicle"],
    }

    for domain, keywords in checks.items():
        if any(keyword in text for keyword in keywords):
            return domain

    return "general"


def improve_features(project_name, design_spec, features):
    features = features or []
    features = [normalize_feature(feature) for feature in features if str(feature).strip()]

    domain = detect_website_type(project_name, design_spec, features)

    if not features:
        return DOMAIN_DEFAULT_PAGES.get(domain, DOMAIN_DEFAULT_PAGES["general"]), domain

    weak_default_sets = [
        ["home", "about", "projects", "skills", "contact"],
        ["home", "about", "projects", "skills", "services", "contact"],
        ["home", "about", "services", "contact"],
    ]

    if features in weak_default_sets and domain != "portfolio":
        return DOMAIN_DEFAULT_PAGES.get(domain, DOMAIN_DEFAULT_PAGES["general"]), domain

    if "home" not in features:
        features.insert(0, "home")

    if "contact" not in features and len(features) < 8:
        features.append("contact")

    return features[:8], domain


def clean_generated_files(files, expected_features):
    if not isinstance(files, dict):
        print("REACT PAGE CLEANER: Output is not dict.")
        return {}

    # Gemini sometimes returns {"files": {...}}
    if isinstance(files.get("files"), dict):
        print("REACT PAGE CLEANER: Found nested files object.")
        files = files["files"]

    expected_map = {}

    for feature in expected_features:
        feature_norm = normalize_feature(feature)
        component = feature_to_component(feature)
        expected_map[feature_norm] = f"src/pages/{component}.jsx"

    print("REACT PAGE CLEANER: Gemini returned keys:", list(files.keys()))
    print("REACT PAGE CLEANER: Expected features:", list(expected_map.keys()))

    cleaned_files = {}

    for path, content in files.items():
        if not isinstance(path, str) or not isinstance(content, str):
            print("REACT PAGE CLEANER: Skipped non-string file:", path)
            continue

        original_path = path
        path = path.replace("\\", "/").strip().lstrip("/")

        if path.startswith("pages/"):
            path = "src/" + path

        if not path.startswith("src/pages/"):
            print("REACT PAGE CLEANER: Skipped unsupported path:", original_path)
            continue

        if not path.endswith(".jsx"):
            print("REACT PAGE CLEANER: Skipped non-JSX file:", original_path)
            continue

        file_name = path.split("/")[-1].replace(".jsx", "")
        file_feature = normalize_feature(file_name)

        # Accept AdmissionsPage.jsx as admissions
        if file_feature.endswith("_page"):
            file_feature = file_feature.replace("_page", "")

        if file_feature not in expected_map:
            print("REACT PAGE CLEANER: Skipped unexpected page:", original_path, "as", file_feature)
            continue

        if "export default" not in content:
            print("REACT PAGE CLEANER: Missing export default:", original_path)
            continue

        # React 17+ can work without import React, but keep it safe
        if "import React" not in content:
            content = 'import React from "react";\n\n' + content

        if "className" not in content:
            print("REACT PAGE CLEANER: Missing className:", original_path)
            continue

        if len(content) < 350:
            print("REACT PAGE CLEANER: Content too small:", original_path, len(content))
            continue

        bad_words = [
            "lorem ipsum",
            "add more here",
            "your content here",
        ]

        if any(bad in content.lower() for bad in bad_words):
            print("REACT PAGE CLEANER: Placeholder content found:", original_path)
            continue

        canonical_path = expected_map[file_feature]
        cleaned_files[canonical_path] = content

    print("REACT PAGE CLEANER: Accepted files:", list(cleaned_files.keys()))

    return cleaned_files

def generate_emergency_fallback_page(project_name, feature, website_type="general", design_spec=None):
    component = feature_to_component(feature)
    title = feature_to_title(feature)

    return f'''import React from "react";

export default function {component}() {{
  const cards = [
    "{title} overview",
    "Key information",
    "Useful details",
    "Next steps"
  ];

  return (
    <main className="page">
      <section className="hero-section premium-hero">
        <p className="eyebrow">{project_name}</p>
        <h1>{title} for a modern {website_type.replace("_", " ")} website.</h1>
        <p>
          This page was generated by Orvix as a safe fallback. It keeps the website
          structured, responsive, and ready for editing even if AI output fails.
        </p>

        <div className="hero-actions">
          <a className="primary-btn" href="/">Explore</a>
          <a className="secondary-btn" href="/contact">Contact</a>
        </div>
      </section>

      <section className="content-grid">
        {{cards.map((card, index) => (
          <div className="card" key={{index}}>
            <span className="card-number">0{{index + 1}}</span>
            <h2>{{card}}</h2>
            <p>
              This section is designed for the {website_type.replace("_", " ")} domain
              and can be expanded with real data, forms, images, dashboards, or APIs.
            </p>
          </div>
        ))}}
      </section>

      <section className="highlight-section">
        <h2>Responsive and presentation ready</h2>
        <p>
          Orvix generated this structure with reusable sections, cards, buttons,
          and clean layout blocks.
        </p>
      </section>
    </main>
  );
}}
'''


def build_fallback_files(project_name, features, design_spec=None, website_type="general"):
    files = {}

    for feature in features:
        component = feature_to_component(feature)
        files[f"src/pages/{component}.jsx"] = generate_emergency_fallback_page(
            project_name,
            feature,
            website_type,
            design_spec
        )

    return files


def build_dynamic_prompt(project_name, design_spec, features, website_type):
    feature_titles = [feature_to_title(feature) for feature in features]

    expected_paths = [
    f"src/pages/{feature_to_component(feature)}.jsx"
    for feature in features
]
    
    return f"""
Return ONLY file blocks. No markdown explanation. No extra text.

Use this exact format for every file:

FILE_START: src/pages/Home.jsx
import React from "react";

export default function Home() {{
  return (
    <main className="page">
      ...
    </main>
  );
}}
FILE_END
You are a senior React frontend developer and product UI designer.

Create complete React JSX page files for a dynamic website.

Project name:
{project_name}

Website type/domain:
{website_type}

Design spec/theme:
{design_spec}

Pages to create exactly:
{feature_titles}


Exact file paths to generate:
{expected_paths}

Required output format:
FILE_START: src/pages/Home.jsx
full React JSX code here
FILE_END

FILE_START: src/pages/About.jsx
full React JSX code here
FILE_END

Rules:
- Return JSON object only.
- Every key must be a file path inside src/pages/.
- Every value must be complete React JSX code as a string.
- Every file must import React.
- Every file must export default component.
- Every component name must match the file name.
- Use className only.
- Do not include CSS inside JSX.
- Do not use Tailwind.
- Do not use external UI libraries.
- Do not import images.
- Do not use lorem ipsum.
- Do not create portfolio content unless website type is portfolio.
- Every page must be unique and domain-specific.
- Make pages attractive, responsive-ready, and card-based.
- Use realistic dummy data arrays and map them into cards/lists.
- Include hero sections, cards, stats, forms, tables, banners, or sections according to page purpose.
- Each page code should be at least 900 characters.

Domain behavior:
- If school: include admissions cards, class levels, teacher cards, campus events, notices, fee/admission details where relevant.
- If hospital: include doctors, departments, appointment form, services, emergency banner, patient care sections where relevant.
- If restaurant: include menu cards, chef sections, reservation form, gallery/review sections where relevant.
- If ecommerce: include product cards, category grid, offers, cart preview, product badges where relevant.
- If real estate: include property cards, agent cards, pricing/location details, gallery sections where relevant.
- If gym: include programs, trainers, pricing, schedule, fitness stats where relevant.
- If travel: include destinations, packages, booking form, hotel/trip cards where relevant.
- If finance: include dashboard panels, transactions, investment cards, secure account sections where relevant.
- If AI tools/SaaS: include feature cards, pricing, agent/tool cards, dashboard-like panels, CTA sections where relevant.

Important:
Create exactly these pages:
{feature_titles}
"""

def build_single_page_prompt(project_name, design_spec, website_type, feature, all_features):
    component = feature_to_component(feature)
    title = feature_to_title(feature)
    all_titles = [feature_to_title(item) for item in all_features]

    return f"""
Return ONLY one React JSX file block. No explanation. No markdown.

Project name:
{project_name}

Website type/domain:
{website_type}

Design spec/theme:
{design_spec}

Current page:
{title}

All website pages:
{all_titles}

Output exactly this format:

FILE_START: src/pages/{component}.jsx
import React from "react";

export default function {component}() {{
  return (
    <main className="page">
      ...
    </main>
  );
}}
FILE_END

Rules:
- Create only the {title} page.
- Component name must be {component}.
- File path must be src/pages/{component}.jsx.
- Use className only.
- No Tailwind.
- No external libraries.
- No image imports.
- No lorem ipsum.
- Make this page attractive, responsive-ready, and card-based.
- Use realistic dummy data arrays and map them into cards/lists.
- Page code should be at least 650 characters.
- Do not create portfolio content unless website type is portfolio.

Domain-specific behavior:
- If school: use admissions cards, classes, teachers, events, notices, fee/admission details where relevant.
- If hospital: use doctors, departments, appointment form, emergency banner, services, patient care sections where relevant.
- If restaurant: use menu cards, chef sections, reservation form, gallery/reviews where relevant.
- If ecommerce: use product cards, categories, offers, cart preview where relevant.
- If SaaS/AI tools: use feature cards, pricing, tools, agent cards, dashboard panels, CTA sections where relevant.
- If general business: use services, benefits, company sections, contact CTA, stats where relevant.

Make the {title} page look unique and useful, not generic.
"""

def generate_batch_page_files(project_name, design_spec, features):
    features, website_type = improve_features(project_name, design_spec, features)

    print("REACT PAGE GENERATOR DOMAIN:", website_type)
    print("REACT PAGE GENERATOR FEATURES:", features)

    generated_files = {}

    for feature in features:
        component = feature_to_component(feature)
        expected_path = f"src/pages/{component}.jsx"

        print(f"REACT PAGE GENERATOR: Generating page with Gemini: {expected_path}")

        prompt = build_single_page_prompt(
            project_name=project_name,
            design_spec=design_spec,
            website_type=website_type,
            feature=feature,
            all_features=features
        )

        try:
            try:
                result = ask_ai(prompt, use_cache=False)
            except TypeError:
                result = ask_ai(prompt)

            print("REACT PAGE GENERATOR AI RESULT:", result.get("success"))
            print("REACT PAGE GENERATOR SOURCE:", result.get("source", "unknown"))
            print("REACT PAGE GENERATOR ERROR:", result.get("error", ""))

            if not result.get("success") or result.get("source") != "gemini":
                print(f"REACT PAGE GENERATOR: Gemini failed for {feature}. Using fallback page.")
                fallback = build_fallback_files(
                    project_name,
                    [feature],
                    design_spec,
                    website_type
                )
                generated_files.update(fallback)
                continue

            files = extract_json(result.get("response", ""))
            cleaned_files = clean_generated_files(files, [feature])

            if expected_path in cleaned_files:
                print(f"REACT PAGE GENERATOR: Gemini page accepted: {expected_path}")
                generated_files[expected_path] = cleaned_files[expected_path]
            elif cleaned_files:
                # Accept first cleaned page if path was normalized differently
                first_path = list(cleaned_files.keys())[0]
                generated_files[expected_path] = cleaned_files[first_path]
                print(f"REACT PAGE GENERATOR: Gemini page accepted with normalized path: {expected_path}")
            else:
                print(f"REACT PAGE GENERATOR: Gemini page invalid for {feature}. Using fallback page.")
                fallback = build_fallback_files(
                    project_name,
                    [feature],
                    design_spec,
                    website_type
                )
                generated_files.update(fallback)

        except Exception as error:
            print(f"REACT PAGE GENERATOR: Exception for {feature}. Using fallback page.")
            print("REACT PAGE GENERATOR ERROR:", error)

            fallback = build_fallback_files(
                project_name,
                [feature],
                design_spec,
                website_type
            )
            generated_files.update(fallback)

    print("REACT PAGE GENERATOR FINAL FILES:", list(generated_files.keys()))

    return generated_files