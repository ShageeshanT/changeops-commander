"""Format a list of incident events into a readable timeline string."""


def format_timeline(events):
    """events: list of (timestamp_str, actor, action)."""
    lines = []
    for ts, actor, action in events:
        lines.append(f"[{ts}] {actor}: {action}")
    return "\n".join(lines)


if __name__ == "__main__":
    out = format_timeline([("10:00", "system", "alert fired"), ("10:02", "shagee", "acknowledged")])
    assert "alert fired" in out and "acknowledged" in out
    print("incident_timeline_formatter: ok")
