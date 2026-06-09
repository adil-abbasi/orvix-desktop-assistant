from app.word_agent.active_word_reader import get_active_document_text
from app.word_agent.word_analyzer import analyze_text
from app.word_agent.word_live_agent import live_insert_text, save_active_document


def detect_document_action(user_command: str):
    text = user_command.lower()

    if "mcq" in text or "mcqs" in text:
        return "mcqs"

    if "summarize" in text or "summary" in text:
        return "summary"

    if "conclusion" in text:
        return "conclusion"

    if "references" in text or "reference" in text:
        return "references"

    if "continue writing" in text or "continue" in text:
        return "continue"

    if "add section" in text or "section" in text:
        return "section"

    if "rewrite" in text or "paraphrase" in text:
        return "rewrite"

    if "study notes" in text or "notes" in text:
        return "notes"

    if "viva" in text:
        return "viva"

    return "generic"


def fallback_document_action(user_command: str, document_text: str):
    action = detect_document_action(user_command)

    title = "Document Update"

    first_lines = [
        line.strip()
        for line in document_text.splitlines()
        if line.strip()
    ]

    if first_lines:
        title = first_lines[0][:80]

    if action == "summary":
        return f"""Summary

This document discusses {title}. The main idea is to explain the topic clearly, highlight its important points, and make the content easier to understand.

The document can be summarized as follows: the topic is useful for learning, practical understanding, and real-world application. It explains important concepts and connects them with benefits, uses, and possible challenges.
"""

    if action == "mcqs":
        return f"""Multiple Choice Questions

1. What is the main focus of this document?
A. Entertainment only
B. Understanding the topic clearly
C. Avoiding practical use
D. Removing learning

Answer: B

2. Why is this topic important?
A. It helps improve understanding
B. It has no practical value
C. It is only theoretical
D. It is not useful

Answer: A

3. Where can this topic be applied?
A. Education
B. Business
C. Technology
D. All of the above

Answer: D

4. What is one benefit of learning this topic?
A. Better decision-making
B. More confusion
C. Less productivity
D. No improvement

Answer: A

5. What should be considered while using this topic?
A. Accuracy
B. Responsibility
C. Practical application
D. All of the above

Answer: D
"""

    if action == "conclusion":
        return f"""Conclusion

In conclusion, {title} is an important topic that helps improve understanding, practical thinking, and problem-solving. It can be useful in education, technology, business, and daily life.

A clear understanding of this topic allows students and professionals to apply concepts more effectively. Therefore, learning and using this topic responsibly can create strong academic and practical value.
"""

    if action == "references":
        return """References

1. Course notes and lecture materials.
2. Academic books related to the topic.
3. Reliable online educational resources.
4. Research articles and professional documentation.
5. Practical examples and case studies.
"""

    if action == "continue":
        return f"""Additional Explanation

Another important point about {title} is that it connects basic understanding with practical use. When a topic is explained step by step, it becomes easier for students and professionals to apply it in real situations.

This also helps in improving confidence, building stronger knowledge, and solving problems in a structured way. With proper learning and careful application, the topic can provide useful results in different fields.
"""

    if action == "notes":
        return f"""Study Notes

Key Points

- The document explains an important topic in a clear way.
- The topic can be useful in academic and practical situations.
- Understanding the basic concepts is important before applying them.
- Real-world examples make the topic easier to understand.
- Responsible and accurate use is important.

Short Explanation

{title} can help improve learning, decision-making, and problem-solving. It is useful because it connects theory with practical application.
"""

    if action == "viva":
        return f"""Viva Questions

1. What is the main topic of this document?
2. Why is this topic important?
3. What are the key concepts discussed in this document?
4. Where can this topic be applied in real life?
5. What are the main benefits of this topic?
6. What are the possible challenges or limitations?
7. How can this topic help students or professionals?
8. What is the conclusion of this document?
"""

    if action == "rewrite":
        return """Rewritten Version

The document explains the topic in a clear and meaningful way. It highlights the main concepts, practical uses, and importance of the subject. The content can help readers understand the topic better and apply it in real-world situations.
"""

    return f"""Additional Section

{title} is an important topic that can be explained further through its purpose, applications, benefits, and challenges. A deeper understanding of this topic helps readers connect the information with practical situations.

This section adds more clarity and supports the overall document by giving extra explanation in a simple and professional way.
"""


def execute_document_action(user_command):
    doc = get_active_document_text()

    if not doc.get("success"):
        return {
            "success": False,
            "message": "No active Word document found."
        }

    document_text = doc.get("text", "")

    prompt = f"""
You are Orvix Document Assistant.

Current document:
{document_text}

User request:
{user_command}

Rules:
- Perform exactly what the user requested.
- Return only the content to insert.
- Do not explain what you are doing.
- Do not repeat existing content unless required.
- Use clean Microsoft Word-friendly text.
- Do not use markdown symbols like **, #, or backticks.
"""

    try:
        result = analyze_text(
            document_text,
            prompt
        )

        if result.get("success") and result.get("response"):
            content = result["response"]
            print("DOCUMENT ACTION: AI content generated successfully.")
        else:
            print("DOCUMENT ACTION: AI failed, using local fallback.")
            print("DOCUMENT ACTION ERROR:", result.get("error", "Unknown AI error"))
            content = fallback_document_action(user_command, document_text)

    except Exception as error:
        print("DOCUMENT ACTION: Exception, using local fallback.")
        print("DOCUMENT ACTION ERROR:", error)
        content = fallback_document_action(user_command, document_text)

    live_insert_text(
        "\n\n" + content,
        delay=0.02,
        chunk_size=6
    )

    try:
        save_active_document(doc.get("path", ""))
    except Exception:
        pass

    return {
        "success": True,
        "message": "Document updated."
    }