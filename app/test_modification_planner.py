from app.project_modifier import modify_project
from app.modification_planner import create_modification_plan

project = modify_project(
    r"C:\Users\adila\OneDrive\Desktop\GoldRecovery3",
    "add login page"
)

plan = create_modification_plan(
    "add login page",
    project["project_files"]
)

print(plan)