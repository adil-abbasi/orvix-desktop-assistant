import re

from app.ai.providers import ask_ai, ask_ai_stream


def clean_ai_word_text(text: str):
    if not text:
        return ""

    # Remove markdown symbols
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("`", "")

    # Convert markdown bullets safely
    text = text.replace("* ", "- ")

    # Remove markdown heading symbols but keep heading text
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)

    # Fix excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def detect_length_instruction(user_command: str):
    text = user_command.lower()

    if any(word in text for word in ["2 page", "2 pages", "two page", "two pages"]):
        return "Write around 900 to 1200 words."

    if any(word in text for word in ["3 page", "3 pages", "three page", "three pages"]):
        return "Write around 1300 to 1700 words."

    if any(word in text for word in ["detailed", "complete", "full", "assignment", "report"]):
        return "Write around 700 to 1000 words."

    if any(word in text for word in ["summary", "short", "brief", "simple"]):
        return "Write around 180 to 300 words."

    return "Write around 400 to 650 words."


def build_word_prompt(user_command, topic, document_type="document"):
    length_rule = detect_length_instruction(user_command)

    return f"""
You are Orvix, an AI desktop assistant writing directly into a Microsoft Word document.

User command:
{user_command}

Detected topic:
{topic}

Detected document type:
{document_type}

Write exactly what the user asked for.

Main rules:
- Follow the user's command, not a fixed template.
- If the user asks for a summary, write only a summary.
- If the user asks for examples, write examples only.
- If the user asks for notes, write notes only.
- If the user asks for advantages and disadvantages, write only those sections.
- If the user asks for report, assignment, essay, detailed, full, 2 pages, or 3 pages, use proper headings.
- Do not force Introduction, Background, Key Concepts, Applications, and Conclusion unless suitable for the user's request.
- Use clean Microsoft Word-friendly text.
- Do not use markdown symbols like **, #, or backticks.
- Do not include any explanation before or after the content.
- Make the content useful, clear, and professional.

Length rule:
{length_rule}

Return only the final document content.
"""


def generate_document_from_user_command(user_command, topic, document_type="document"):
    """
    Non-streaming fallback.
    This waits for the full AI response before writing.
    Keep this for backup use.
    """

    prompt = build_word_prompt(user_command, topic, document_type)

    result = ask_ai(prompt, use_cache=False)

    if result.get("success"):
        response = result.get("response", "").strip()

        if response:
            return clean_ai_word_text(response)

    error = result.get("error", "Unknown AI error")

    return (
        "AI generation failed.\n"
        f"Error: {error}"
    )


def stream_document_from_user_command(user_command, topic, document_type="document"):
    """
    Streaming version.
    This sends AI chunks one by one so Word can write while AI is still generating.
    """

    prompt = build_word_prompt(user_command, topic, document_type)

    for chunk in ask_ai_stream(prompt):
        if not chunk.get("success"):
            yield (
                "AI generation failed.\n"
                f"Error: {chunk.get('error', 'Unknown error')}"
            )
            return

        text = clean_ai_word_text(chunk.get("text", ""))

        if text:
            yield text