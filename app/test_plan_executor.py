from app.project_spec_generator import generate_project_spec
from app.ai_plan_schema import validate_plan
from app.plan_executor import execute_plan


spec = generate_project_spec(
    "build hospital website with doctor dashboard patient records appointments dark theme"
)

validation = validate_plan(spec)

if validation["valid"]:
    result = execute_plan(spec)

    print(result["success"])
    print(result["name"])
    print(result["template"])
else:
    print(validation)