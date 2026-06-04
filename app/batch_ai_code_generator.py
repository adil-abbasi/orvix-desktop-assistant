import json
import re

from app.ai.providers import ask_ai


def extract_json(text: str):
    if not text:
        return None

    text = text.strip()

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


def generate_batch_page_files(project_name, design_spec, features):
    prompt = f"""
Return ONLY valid JSON.

Generate React JSX page files for this project.

Project name: {project_name}
Design spec: {design_spec}
Features: {features}

JSON format:
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
- Use project industry and theme.
"""

    result = ask_ai(prompt)

    if not result.get("success"):
        return {}

    files = extract_json(result.get("response", ""))

    if isinstance(files, dict):
        return files

    return {}