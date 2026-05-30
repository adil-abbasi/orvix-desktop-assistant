from app.project_spec_generator import generate_project_spec
from app.ai_plan_schema import validate_plan


spec = generate_project_spec(
    "build hospital website with doctor dashboard patient records appointments dark theme"
)

result = validate_plan(spec)

print(spec)
print(result)