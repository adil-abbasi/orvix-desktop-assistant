from app.word_agent.word_live_writer import create_live_ai_document

result = create_live_ai_document(
    topic="cybersecurity",
    filename="LiveCyberResearch",
    document_type="research report"
)

print(result)