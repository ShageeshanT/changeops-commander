"""State machine enforcing valid incident status transitions."""

VALID_TRANSITIONS = {
    "detected": {"investigating"},
    "investigating": {"identified", "resolved"},
    "identified": {"monitoring", "resolved"},
    "monitoring": {"resolved", "investigating"},
    "resolved": set(),
}


def can_transition(current: str, target: str) -> bool:
    return target in VALID_TRANSITIONS.get(current, set())


if __name__ == "__main__":
    assert can_transition("detected", "investigating") is True
    assert can_transition("resolved", "investigating") is False
    print("incident_status_transitions: ok")
