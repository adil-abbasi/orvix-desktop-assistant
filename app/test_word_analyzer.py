from app.word_agent.word_memory import load_current_document
from app.word_agent.word_reader import read_word_document
from app.word_agent.word_analyzer import analyze_text

path = load_current_document()
doc = read_word_document(path)

result = analyze_text(
    doc["text"],
    "Summarize this document and create 5 questions with answers."
)

print(result)