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
        except Exception as e:
            print("DEBUG JSON PARSE ERROR:", e)
            return None

    print("DEBUG NO JSON FOUND IN RESPONSE")
    return None


def generate_design_spec(user_request: str):
    prompt = f"""
Return only valid JSON.

Create a design specification for this request.

JSON schema:
{{
  "industry": "string",
  "style": "string",
  "theme": {{
    "primary": "#000000",
    "secondary": "#D4AF37",
    "mode": "dark"
  }},
  "pages": ["Home", "Listings", "Agents", "Contact"],
  "landing_sections": ["Hero", "Featured Listings", "Testimonials", "Contact CTA"]
}}

User request:
{user_request}
"""

    result = ask_ai(prompt)

    print("DEBUG DESIGN RESULT:", result)

    if not result.get("success"):
        return None

    response = result.get("response", "")

    return extract_json(response)