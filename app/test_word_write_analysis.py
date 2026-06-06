from app.word_agent.word_memory import load_current_document
from app.word_agent.word_reader import read_word_document
from app.word_agent.word_analyzer import analyze_text
from app.word_agent.word_writer import append_to_word_document

path = load_current_document()
doc = read_word_document(path)

analysis = analyze_text(
    doc["text"],
    "Create 5 questions with answers from this document."
)

if analysis["success"]:
    result = append_to_word_document(
        path,
        "Questions and Answers",
        analysis["response"]
    )

    print(result)
else:
    print(analysis)
    