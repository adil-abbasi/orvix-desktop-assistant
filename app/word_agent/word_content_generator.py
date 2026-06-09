import re

from app.ai.providers import ask_ai, ask_ai_stream


def clean_ai_word_text(text: str):
    if not text:
        return ""

    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("`", "")
    text = text.replace("* ", "- ")

    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
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


def fallback_word_content(topic, user_command="", document_type="document"):
    topic_title = topic.strip().title() if topic else "Generated Document"
    command = user_command.lower()

    if "summary" in command or "summarize" in command:
        return f"""{topic_title}

Summary

{topic_title} is an important topic that helps people understand modern ideas, systems, and practical applications. It is useful in education, technology, business, and daily life.

In simple words, {topic_title} explains how concepts work, why they matter, and how they can be applied to solve real problems. A clear understanding of this topic can help students and professionals improve their knowledge and make better decisions.
"""

    if "mcq" in command or "mcqs" in command:
        return f"""{topic_title}

Multiple Choice Questions

1. What is the main purpose of {topic_title}?
A. To create confusion
B. To understand and solve problems
C. To avoid learning
D. To remove technology

Answer: B

2. Why is {topic_title} important?
A. It has no real use
B. It only works in theory
C. It helps in practical understanding
D. It is used only for entertainment

Answer: C

3. Where can {topic_title} be applied?
A. Education
B. Business
C. Technology
D. All of the above

Answer: D

4. What is one benefit of learning {topic_title}?
A. Better understanding
B. Poor decision-making
C. Less productivity
D. No improvement

Answer: A

5. What should be considered while using {topic_title}?
A. Accuracy
B. Ethics
C. Practical use
D. All of the above

Answer: D
"""

    if "advantages" in command or "disadvantages" in command or "benefits" in command:
        return f"""{topic_title}

Advantages

1. {topic_title} helps improve understanding and decision-making.
2. It can save time by organizing information clearly.
3. It supports learning, productivity, and practical problem-solving.
4. It can be used in education, business, technology, and research.

Disadvantages

1. It may require proper knowledge and skills.
2. Incorrect use can create confusion or unreliable results.
3. Some applications may involve cost, privacy, or technical challenges.
4. It should be used carefully and responsibly.

Conclusion

{topic_title} has many useful advantages, but it also has some limitations. A balanced and responsible approach is important for getting the best results.
"""

    if "examples" in command or "example" in command:
        return f"""{topic_title}

Examples

1. Education

{topic_title} can be used in education to explain concepts, support learning, and help students understand difficult topics.

2. Business

In business, {topic_title} can help organize information, improve planning, and support better decision-making.

3. Technology

In technology, {topic_title} can be used to build systems, improve automation, and solve practical problems.

4. Daily Life

In daily life, {topic_title} can help people save time, understand information, and complete tasks more efficiently.

Conclusion

These examples show that {topic_title} is useful in many areas and can be applied in both academic and practical situations.
"""

    if "notes" in command or "study notes" in command:
        return f"""{topic_title}

Study Notes

Meaning

{topic_title} is a useful topic that helps people understand ideas, systems, and practical applications.

Important Points

- It is useful for learning and problem-solving.
- It can be applied in education, business, technology, and daily life.
- It helps improve understanding and decision-making.
- It should be used carefully and responsibly.

Applications

{topic_title} can be used in different fields to improve productivity, organize information, and solve real-world problems.

Conclusion

{topic_title} is important because it connects theory with practical use.
"""

    return f"""{topic_title}

Introduction

{topic_title} is an important topic in modern education, technology, and professional life. It helps people understand ideas clearly and apply them in practical situations.

Key Concepts

The main concepts of {topic_title} include understanding its purpose, how it works, and where it can be used. These concepts make the topic easier to learn and apply.

Applications

{topic_title} can be used in many areas such as education, business, technology, research, and daily life. It helps improve productivity, decision-making, and problem-solving.

Benefits

The main benefits of {topic_title} include better understanding, improved efficiency, and practical use in real-world situations. It can also help students and professionals build stronger knowledge.

Conclusion

In conclusion, {topic_title} is useful and practical. Learning this topic can help people improve their skills, solve problems, and understand modern systems more effectively.
"""


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
- If the user asks for MCQs, write MCQs with answers.
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
    Non-streaming version.
    Tries AI first. If AI fails, returns local fallback content.
    """

    prompt = build_word_prompt(user_command, topic, document_type)

    try:
        try:
            result = ask_ai(prompt, use_cache=False)
        except TypeError:
            result = ask_ai(prompt)

        if result.get("success"):
            response = result.get("response", "").strip()

            if response:
                print("WORD: AI content generated successfully.")
                return clean_ai_word_text(response)

        print("WORD: AI failed, using local fallback.")
        print("WORD AI ERROR:", result.get("error", "Unknown AI error"))

        return fallback_word_content(topic, user_command, document_type)

    except Exception as error:
        print("WORD: AI exception, using local fallback.")
        print("WORD ERROR:", error)

        return fallback_word_content(topic, user_command, document_type)


def stream_document_from_user_command(user_command, topic, document_type="document"):
    """
    Streaming version.
    Tries AI streaming first. If AI streaming fails, streams local fallback content.
    """

    prompt = build_word_prompt(user_command, topic, document_type)

    try:
        print("WORD STREAM: Trying AI provider...")

        has_output = False

        for chunk in ask_ai_stream(prompt):
            if not chunk.get("success"):
                print("WORD STREAM: AI failed, using local fallback.")
                print("WORD STREAM ERROR:", chunk.get("error", "Unknown error"))

                yield fallback_word_content(topic, user_command, document_type)
                return

            text = clean_ai_word_text(chunk.get("text", ""))

            if text:
                has_output = True
                yield text

        if not has_output:
            print("WORD STREAM: AI returned empty output, using local fallback.")
            yield fallback_word_content(topic, user_command, document_type)

    except Exception as error:
        print("WORD STREAM: Exception, using local fallback.")
        print("WORD STREAM ERROR:", error)

        yield fallback_word_content(topic, user_command, document_type)