from app.project_spec_generator import generate_project_spec
from app.plan_enhancer import enhance_plan

spec = generate_project_spec(
    "build hospital website with doctor dashboard patient records appointments dark theme"
)

enhanced = enhance_plan(spec)

print(enhanced)