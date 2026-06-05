from app.word_agent.word_memory import load_current_document
from app.word_agent.word_reader import read_word_document

path = load_current_document()

print("PATH:")
print(path)

result = read_word_document(path)

print("\nWORDS:")
print(result["words"])

print("\nTEXT:")
print(result["text"])