from app.ai.providers import ask_ai

prompt = "Say hello from Orvix in one short sentence."

print("First call:")
print(ask_ai(prompt))

print("Second call should use cache:")
print(ask_ai(prompt))