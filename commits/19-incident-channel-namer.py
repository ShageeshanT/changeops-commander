"""Generate a consistent chat channel name for an incident."""

import re


def channel_name(incident_id: str, title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"inc-{incident_id.lower()}-{slug}"[:80]


if __name__ == "__main__":
    name = channel_name("INC-1024", "API Latency Spike!")
    assert name.startswith("inc-inc-1024-api-latency-spike")
    print("incident_channel_namer: ok")
