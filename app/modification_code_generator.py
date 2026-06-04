import json
import re

from app.ai.providers import ask_ai


def extract_json(text):
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


def generate_file_changes(request, project_files, modification_plan):
    compact_files = {}

    for path, content in project_files.items():
        compact_files[path] = content[:4000]

    prompt = f"""
Return ONLY valid JSON. No markdown. No explanation.

You are Orvix AI code editor.

User request:
{request}

Modification plan:
{modification_plan}

Existing project files:
{compact_files}

Return JSON in this exact format:
{{
  "src/pages/Login.jsx": "full file code here",
  "src/App.jsx": "full updated file code here"
}}

Rules:
- Keys must be relative project paths.
- Values must be full file contents.
- Do not use absolute Windows paths.
- Do not include markdown fences.
- Preserve existing functionality.
- If you create a new page, also update routing if needed.
- Use valid React JSX only.
"""

    result = ask_ai(prompt)

    if not result.get("success"):
        return {}

    parsed = extract_json(result.get("response", ""))

    if isinstance(parsed, dict):
        return parsed

    return {}