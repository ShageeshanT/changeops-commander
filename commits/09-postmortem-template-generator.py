"""Generate a blank postmortem markdown template for an incident."""


def generate_postmortem_template(incident_id: str, title: str) -> str:
    return f"""# Postmortem: {title} ({incident_id})

## Summary


## Timeline


## Root Cause


## Impact


## What Went Well


## What Went Wrong


## Action Items
- [ ]
"""


if __name__ == "__main__":
    doc = generate_postmortem_template("INC-1024", "API latency spike")
    assert "INC-1024" in doc and "Root Cause" in doc
    print("postmortem_template_generator: ok")
