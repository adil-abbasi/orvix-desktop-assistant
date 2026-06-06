from app.task_router import detect_task_type

commands = [
    "build react website named Store",
    "modify current project and add login page",
    "create MS Word file named Cyber about cybersecurity",
    "make 20 MCQs",
    "create presentation from current document",
    "create excel sheet for student marks"
]

for command in commands:
    print(command, "=>", detect_task_type(command))