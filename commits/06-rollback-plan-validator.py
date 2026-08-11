"""Validate a rollback plan has the required fields before execution."""

REQUIRED_FIELDS = ("service", "target_version", "steps", "approver")


def validate_rollback_plan(plan: dict):
    missing = [f for f in REQUIRED_FIELDS if not plan.get(f)]
    if missing:
        return False, f"missing fields: {', '.join(missing)}"
    if not isinstance(plan["steps"], list) or not plan["steps"]:
        return False, "steps must be a non-empty list"
    return True, "ok"


if __name__ == "__main__":
    ok, msg = validate_rollback_plan({"service": "api", "target_version": "1.2.3", "steps": ["deploy"], "approver": "shagee"})
    assert ok, msg
    print("rollback_plan_validator: ok")
