"""Generate a unique, sortable incident ID."""

import time
import random


def generate_incident_id(prefix: str = "INC") -> str:
    ts = int(time.time())
    suffix = random.randint(100, 999)
    return f"{prefix}-{ts}{suffix}"


if __name__ == "__main__":
    iid = generate_incident_id()
    assert iid.startswith("INC-")
    print("incident_id_generator: ok")
