import re


def extract_number(text, default=10):
    match = re.search(r"\b(\d+)\b", text)

    if match:
        return int(match.group(1))

    return default


def detect_task_type(text):
    text = text.lower()

    if "mcq" in text or "mcqs" in text:
        return "mcqs"

    if "viva" in text:
        return "viva_questions"

    if "question" in text or "questions" in text:
        return "questions_answers"

    if "summarize" in text or "summary" in text:
        return "summary"

    if "paraphrase" in text:
        return "paraphrase"

    if "conclusion" in text:
        return "conclusion"

    return "analysis"


def build_document_task_prompt(user_command):
    count = extract_number(user_command)
    task_type = detect_task_type(user_command)

    if task_type == "mcqs":
        return (
            f"Create {count} MCQs from this document. "
            "Each MCQ must have 4 options A-D and clearly mention the correct answer."
        )

    if task_type == "viva_questions":
        return f"Create {count} viva questions with short answers from this document."

    if task_type == "questions_answers":
        return f"Create {count} questions with answers from this document."

    if task_type == "summary":
        return "Summarize this document clearly with headings and key points."

    if task_type == "paraphrase":
        return "Paraphrase this document professionally while preserving meaning."

    if task_type == "conclusion":
        return "Write a strong conclusion for this document."

    return user_command