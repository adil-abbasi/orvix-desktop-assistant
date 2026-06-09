import ollama


MODEL_NAME = "llama3.2:1b"


def clean_ollama_response(text: str):
    if not text:
        return ""

    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("`", "")

    # Some reasoning models may return thinking tags
    text = text.replace("<think>", "")
    text = text.replace("</think>", "")

    return text.strip()


def ask_ollama(prompt: str):
    try:
        print(f"OLLAMA: Trying local model: {MODEL_NAME}")

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Orvix local fallback AI. "
                        "Give clean, useful, direct output. "
                        "Do not use markdown unless requested. "
                        "Do not explain your process."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 900
            }
        )

        content = response.get("message", {}).get("content", "")
        content = clean_ollama_response(content)

        if not content:
            return {
                "success": False,
                "response": "",
                "error": "Ollama returned empty response.",
                "source": "ollama"
            }

        print("OLLAMA: Response generated successfully.")

        return {
            "success": True,
            "response": content,
            "error": "",
            "source": "ollama"
        }

    except Exception as error:
        print("OLLAMA: Failed.")
        print("OLLAMA ERROR:", error)

        return {
            "success": False,
            "response": "",
            "error": str(error),
            "source": "ollama"
        }