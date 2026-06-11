import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY", "").strip()
GROK_MODEL = os.getenv("GROK_MODEL", "grok-build-0.1").strip()
GROK_API_URL = "https://api.x.ai/v1/chat/completions"


def ask_grok(prompt: str, system_prompt: str = "", temperature: float = 0.3):
    if not GROK_API_KEY:
        return {
            "success": False,
            "response": "",
            "error": "No GROK_API_KEY found.",
            "source": "grok"
        }

    messages = []

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    try:
        response = requests.post(
            GROK_API_URL,
            headers={
                "Authorization": f"Bearer {GROK_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROK_MODEL,
                "messages": messages,
                "temperature": temperature,
            },
            timeout=90,
        )

        if response.status_code >= 400:
            return {
                "success": False,
                "response": "",
                "error": f"Grok API error {response.status_code}: {response.text}",
                "source": "grok"
            }

        data = response.json()

        text = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        if not text:
            return {
                "success": False,
                "response": "",
                "error": "Grok returned empty response.",
                "source": "grok"
            }

        return {
            "success": True,
            "response": text,
            "error": "",
            "source": "grok"
        }

    except Exception as error:
        return {
            "success": False,
            "response": "",
            "error": str(error),
            "source": "grok"
        }