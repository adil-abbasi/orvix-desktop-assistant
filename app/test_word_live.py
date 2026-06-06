from app.word_agent.word_live_agent import open_or_create_document, live_insert_text

open_or_create_document()

live_insert_text(
    """Cybersecurity Research

Introduction
Cybersecurity protects systems, networks, and data from digital attacks.

Types of Threats
Common threats include phishing, malware, ransomware, and social engineering.

Conclusion
Cybersecurity is essential for individuals, businesses, and governments.""",
    delay=0.3
)