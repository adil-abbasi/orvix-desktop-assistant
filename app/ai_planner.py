import json
import re

from app.project_spec_generator import generate_project_spec
from app.ai.providers import ask_ai
from app.project_design_spec import generate_design_spec

def extract_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None

    return None


def build_planner_prompt(user_request: str):
    return f"""
You are Orvix AI planner.

Convert the user request into ONLY valid JSON.

Required JSON format:
{{
  "project_type": "react app",
  "name": "ProjectName",
  "features": ["feature_one", "feature_two"],
  "theme": "default"
}}

Rules:
- Return JSON only.
- No explanation.
- project_type must be one of: react app, ml project, node express app, django app, flask app, spring boot app.
- Use snake_case for features.
- Infer a clean project name.
- Keep the name short and folder-safe.
- If user asks for website/system/dashboard/portal, use react app.
- If user asks for prediction/data science/model/training, use ml project.

User request:
{user_request}
"""


def create_rule_based_plan(user_request: str):
    return generate_project_spec(user_request)


def create_ai_plan(user_request: str):
    prompt = build_planner_prompt(user_request)

    result = ask_ai(prompt)

    if not result.get("success"):
        return None

    parsed = extract_json(result.get("response", ""))

    return parsed


def create_project_plan(user_request: str):
    ai_plan = create_ai_plan(user_request)

    if ai_plan:
        ai_plan["raw_request"] = user_request

        design_spec = generate_design_spec(user_request)

        if design_spec:
            ai_plan["design_spec"] = design_spec

            if not ai_plan.get("features"):
                features = []

                for page in design_spec.get("pages", []):
                    feature = (
                        page.lower()
                        .replace("&", "")
                        .replace("/", " ")
                        .replace("-", "_")
                        .replace(" ", "_")
                        .replace("__", "_")
                        .strip("_")
                    )

                    if feature and feature != "home":
                        features.append(feature)

                ai_plan["features"] = features

        return ai_plan

    return create_rule_based_plan(user_request)