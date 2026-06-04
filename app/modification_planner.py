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
        except Exception as e:
            print("DEBUG MOD JSON ERROR:", e)
            return None

    print("DEBUG MOD NO JSON FOUND")
    return None


def create_modification_plan(request, project_files):
    file_list = list(project_files.keys())

    prompt = f"""
Return only valid JSON. No markdown. No explanation.

You are Orvix AI project modification planner.

User request:
{request}

Existing project files:
{file_list}

Required JSON format:
{{
  "action": "modify_project",
  "files_to_create": [
    "src/pages/Login.jsx"
  ],
  "files_to_modify": [
    "src/App.jsx"
  ],
  "summary": "short summary"
}}

Rules:
- Use relative paths only.
- If adding a page, include it in files_to_create.
- If route/navigation needs update, include src/App.jsx in files_to_modify.
- Do not include absolute Windows paths.
"""

    result = ask_ai(prompt)

    print("DEBUG MOD RESULT:", result)

    if not result.get("success"):
        return None

    return extract_json(result.get("response", ""))