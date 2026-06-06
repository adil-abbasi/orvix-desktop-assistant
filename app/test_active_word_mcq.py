from app.word_agent.active_word_analyzer import analyze_active_document
from app.word_agent.task_parser import build_document_task_prompt

user_command = "analyze current document and make 20 MCQs"

task = build_document_task_prompt(user_command)

result = analyze_active_document(task)

if result.get("success"):
    print(result["response"])
else:
    print(result)