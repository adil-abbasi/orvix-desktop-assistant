import json
import re

from app.ai.providers import ask_ai


def extract_json(text: str):
    if not text:
        return None

    text = text.strip()

    # Remove markdown fences if AI returns ```json ... ```
    text = re.sub(r"^```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*\}", text)

    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None

    return None


def feature_to_component(feature: str):
    parts = (
        feature.replace("-", "_")
        .replace(" ", "_")
        .split("_")
    )

    return "".join(
        part.capitalize()
        for part in parts
        if part.strip()
    )


def feature_to_title(feature: str):
    return (
        feature.replace("_", " ")
        .replace("-", " ")
        .title()
    )


def generate_fallback_page(project_name, feature, design_spec=None):
    """
    Safety fallback.
    Used only when AI fails/quota/invalid JSON.
    This prevents empty projects.
    """

    component = feature_to_component(feature)
    title = feature_to_title(feature)

    theme = "modern"
    tone = "professional"

    if isinstance(design_spec, dict):
        theme = design_spec.get("theme", theme)
        tone = design_spec.get("tone", tone)

    return f"""import React from "react";

export default function {component}() {{
  return (
    <main className="page {feature}">
      <section className="hero-section">
        <p className="eyebrow">{project_name}</p>
        <h1>{title}</h1>
        <p>
          This page is designed for a {tone} {theme} experience. It provides
          clear information, useful sections, and a clean interface for users.
        </p>
      </section>

      <section className="content-grid">
        <div className="card">
          <h2>Overview</h2>
          <p>
            The {title} section helps users understand the purpose of this
            feature and how it supports the overall project.
          </p>
        </div>

        <div className="card">
          <h2>Key Benefits</h2>
          <p>
            It improves usability, organizes important information, and gives
            the application a more complete and professional structure.
          </p>
        </div>

        <div className="card">
          <h2>Next Step</h2>
          <p>
            This page can be expanded with real data, forms, dashboards,
            authentication, or backend API integration.
          </p>
        </div>
      </section>
    </main>
  );
}}
"""


def build_fallback_files(project_name, features, design_spec=None):
    files = {}

    for feature in features:
        component = feature_to_component(feature)
        files[f"src/pages/{component}.jsx"] = generate_fallback_page(
            project_name,
            feature,
            design_spec
        )

    return files


def generate_batch_page_files(project_name, design_spec, features):
    if not features:
        return {}

    # Limit pages for one AI call, otherwise JSON becomes too large/fragile.
    features = features[:6]

    prompt = f"""
Return ONLY valid JSON.

Generate React JSX page files for this project.

Project name:
{project_name}

Design spec:
{design_spec}

Features:
{features}

Required JSON format:
{{
  "src/pages/Home.jsx": "full React JSX code",
  "src/pages/About.jsx": "full React JSX code"
}}

Rules:
- JSON only.
- No markdown.
- No explanation.
- Every file must export default component.
- No external libraries.
- Use className only.
- Use simple React JSX.
- Make content meaningful, not placeholder.
- Use project industry, theme, and feature names.
- Every feature must have one page file.
- Do not include CSS in JSX.
- Do not import images.
"""

    result = ask_ai(prompt, use_cache=False)

    if not result.get("success"):
        return build_fallback_files(
            project_name,
            features,
            design_spec
        )

    files = extract_json(result.get("response", ""))

    if isinstance(files, dict) and files:
        cleaned_files = {}

        for path, content in files.items():
            if not isinstance(path, str) or not isinstance(content, str):
                continue

            if not path.startswith("src/pages/"):
                continue

            if not path.endswith(".jsx"):
                continue

            if "export default" not in content:
                continue

            cleaned_files[path] = content

        if cleaned_files:
            return cleaned_files

    return build_fallback_files(
        project_name,
        features,
        design_spec
    )