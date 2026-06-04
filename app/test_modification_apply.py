from app.project_modifier import modify_project
from app.modification_planner import create_modification_plan
from app.modification_code_generator import generate_file_changes
from app.modification_executor import apply_file_changes

project_path = r"C:\Users\adila\OneDrive\Desktop\GoldRecovery3"
request = "add login page with email, password, remember me and forgot password"

project = modify_project(project_path, request)

plan = create_modification_plan(
    request,
    project["project_files"]
)

print("PLAN:")
print(plan)

changes = generate_file_changes(
    request,
    project["project_files"],
    plan
)

print("CHANGES:")
print(changes.keys())

result = apply_file_changes(
    project_path,
    changes
)

print("RESULT:")
print(result)