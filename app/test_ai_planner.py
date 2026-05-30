from app.ai_planner import create_project_plan

plan = create_project_plan(
    "build hospital website with doctor dashboard patient records appointments dark theme"
)

print(plan)