"""Format a short incident summary suitable for a chat post."""


def format_summary(incident_id: str, severity: str, title: str, status: str) -> str:
    return f"[{severity}] {incident_id} \u2014 {title} (status: {status})"


if __name__ == "__main__":
    out = format_summary("INC-1024", "SEV2", "Checkout errors", "investigating")
    assert "INC-1024" in out and "SEV2" in out
    print("incident_summary_formatter: ok")
