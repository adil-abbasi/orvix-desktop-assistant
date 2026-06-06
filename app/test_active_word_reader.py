from app.word_agent.active_word_reader import get_active_document_text

result = get_active_document_text()

print(result["text"][:1000])