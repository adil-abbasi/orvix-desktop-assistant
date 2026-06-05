from app.word_agent.word_creator import create_word_document

result = create_word_document(
    name="CyberSecurityResearch",
    title="Cybersecurity Research",
    content="This document was created by Orvix."
)

print(result)