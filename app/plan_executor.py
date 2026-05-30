from app.plan_project_builder import build_project_from_plan


def execute_plan(plan):
    location = plan.get("location", "desktop")

    return build_project_from_plan(plan, location)