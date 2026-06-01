import ollama

MODEL_NAME = "qwen3:1.7b"


def ask_ollama(prompt: str):
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return {
            "success": True,
            "response": response["message"]["content"],
            "error": ""
        }

    except Exception as e:
        return {
            "success": False,
            "response": "",
            "error": str(e)
        }