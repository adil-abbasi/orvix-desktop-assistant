from app.ai.providers import ask_ai


def generate_document_content(topic, document_type="report"):
    prompt = f"""
Create a professional {document_type} about:

{topic}

Requirements:
- Proper introduction
- Multiple useful sections
- Clear explanation
- Practical examples where useful
- Conclusion
- Plain text only
"""

    result = ask_ai(prompt)

    if result.get("success"):
        return result["response"]

    return f"Unable to generate content about {topic}"