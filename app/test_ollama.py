from app.ai.ollama_provider import ask_ollama

print("Testing Ollama...")

result = ask_ollama(
    "Say hello from Orvix in one short sentence."
)

print(result)