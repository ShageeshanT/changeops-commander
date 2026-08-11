"""Export incident data into a markdown report string."""


def export_report(incident: dict) -> str:
    lines = [f"# Incident Report: {incident.get('id', 'UNKNOWN')}", ""]
    for key in ("title", "severity", "status", "detected_at", "resolved_at", "owner"):
        if key in incident:
            lines.append(f"- **{key.replace('_', ' ').title()}**: {incident[key]}")
    return "\n".join(lines)


if __name__ == "__main__":
    report = export_report({"id": "INC-1024", "title": "Checkout errors", "severity": "SEV2"})
    assert "INC-1024" in report and "Severity" in report
    print("incident_report_exporter: ok")
