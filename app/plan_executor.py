from app.plan_enhancer import enhance_plan
from app.plan_project_builder import build_project_from_plan


def execute_plan(plan):
    enhanced_plan = enhance_plan(plan)

    location = enhanced_plan.get("location", "desktop")

    return build_project_from_plan(enhanced_plan, location)