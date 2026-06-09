from app.ai.providers import ask_ai


def clean_response(text: str):
    if not text:
        return ""

    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("`", "")
    text = text.replace("#", "")

    return text.strip()


def fallback_analysis_response(text, task):
    command = task.lower()
    title = "the document"

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if lines:
        title = lines[0][:80]

    if "summarize" in command or "summary" in command:
        return f"""Summary

This document discusses {title}. The main purpose of the document is to explain the topic clearly and make it easier to understand.

The content highlights important points, practical uses, and general benefits. Overall, the document is useful for learning, revision, and basic understanding of the topic.
"""

    if "mcq" in command or "mcqs" in command:
        return f"""Multiple Choice Questions

1. What is the main purpose of this document?
A. To confuse the reader
B. To explain the topic clearly
C. To avoid learning
D. To remove important information

Answer: B

2. What can the reader gain from this document?
A. Better understanding
B. Less knowledge
C. No practical value
D. More confusion

Answer: A

3. Where can the topic be applied?
A. Education
B. Technology
C. Business
D. All of the above

Answer: D

4. Why is this topic useful?
A. It supports learning and problem-solving
B. It has no real use
C. It only creates difficulty
D. It is not practical

Answer: A

5. What is important while using this topic?
A. Accuracy
B. Responsibility
C. Practical understanding
D. All of the above

Answer: D
"""

    if "conclusion" in command:
        return f"""Conclusion

In conclusion, {title} is an important topic that helps improve understanding and practical knowledge. It can be useful in education, technology, business, and daily life.

A clear understanding of this topic allows learners to apply ideas more effectively and solve problems in a better way.
"""

    if "references" in command or "reference" in command:
        return """References

1. Course notes and lecture materials.
2. Academic books related to the topic.
3. Reliable online educational resources.
4. Research articles and professional documentation.
5. Practical examples and case studies.
"""

    if "rewrite" in command or "paraphrase" in command:
        return f"""Rewritten Version

This document explains {title} in a clear and meaningful way. It presents important ideas, practical applications, and useful points that can help readers understand the topic more effectively.
"""

    if "viva" in command:
        return """Viva Questions

1. What is the main topic of this document?
2. Why is this topic important?
3. What are the key concepts discussed?
4. What are the real-world applications?
5. What are the benefits of this topic?
6. What challenges can occur while using it?
7. How can this topic help students or professionals?
8. What is the conclusion of the document?
"""

    return f"""Document Analysis

This document discusses {title}. It explains the topic in a clear way and provides useful information for understanding the subject.

The content can be improved by adding examples, practical applications, benefits, challenges, and a short conclusion. These additions will make the document more complete and professional.
"""


def analyze_text(text, task):
    prompt = f"""
You are Orvix document assistant.

Task:
{task}

Document text:
{text}

Rules:
- Return a clear, useful response.
- Do not use markdown symbols like **, #, or backticks.
- Keep the response Word-friendly.
- Do not explain what you are doing.
"""

    try:
        try:
            result = ask_ai(prompt, use_cache=False)
        except TypeError:
            result = ask_ai(prompt)

        if result.get("success"):
            response = clean_response(result.get("response", ""))

            if response:
                print("WORD ANALYZER: AI response generated successfully.")

                return {
                    "success": True,
                    "response": response,
                    "source": "ai"
                }

        print("WORD ANALYZER: AI failed, using fallback.")
        print("WORD ANALYZER ERROR:", result.get("error", "AI failed"))

        return {
            "success": True,
            "response": fallback_analysis_response(text, task),
            "source": "fallback"
        }

    except Exception as error:
        print("WORD ANALYZER: Exception, using fallback.")
        print("WORD ANALYZER ERROR:", error)

        return {
            "success": True,
            "response": fallback_analysis_response(text, task),
            "source": "fallback"
        }