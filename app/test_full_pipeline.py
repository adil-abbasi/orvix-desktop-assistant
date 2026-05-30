from app.project_spec_generator import generate_project_spec
from app.ai_plan_schema import validate_plan
from app.plan_executor import execute_plan

request = (
    "build hospital website with "
    "doctor dashboard patient records appointments dark theme"
)

spec = generate_project_spec(request)

print("SPEC:")
print(spec)

validation = validate_plan(spec)

print("VALIDATION:")
print(validation)

if validation["valid"]:
    result = execute_plan(spec)

    print("RESULT:")
    print(result["success"])
    print(result["name"])