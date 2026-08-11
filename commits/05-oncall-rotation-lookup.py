"""Find the current on-call engineer from a weekly rotation schedule."""

from datetime import datetime


def current_oncall(rotation, now=None):
    """rotation: list of (weekday_index, name), weekday_index 0=Monday."""
    now = now or datetime.utcnow()
    for weekday, name in rotation:
        if weekday == now.weekday():
            return name
    return rotation[0][1] if rotation else None


if __name__ == "__main__":
    schedule = [(0, "Asha"), (1, "Bimal"), (2, "Chamath")]
    assert current_oncall(schedule, datetime(2026, 8, 11)) == "Bimal"
    print("oncall_rotation_lookup: ok")
