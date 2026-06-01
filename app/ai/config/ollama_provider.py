import subprocess


MODEL_NAME = "qwen3:4b"


def ask_ollama(prompt: str):
    try:
        result = subprocess.run(
            ["ollama", "run", MODEL_NAME, prompt],
            capture_output=True,
            text=True,
            timeout=120
        )

        return {
            "success": result.returncode == 0,
            "response": result.stdout.strip(),
            "error": result.stderr.strip()
        }

    except Exception as e:
        return {
            "success": False,
            "response": "",
            "error": str(e)
        }