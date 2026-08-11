"""Map incident severity to its required response SLA in minutes."""

SEVERITY_SLA_MINUTES = {"SEV1": 5, "SEV2": 15, "SEV3": 60, "SEV4": 240}


def response_sla_minutes(severity: str) -> int:
    return SEVERITY_SLA_MINUTES.get(severity, 240)


if __name__ == "__main__":
    assert response_sla_minutes("SEV1") == 5
    assert response_sla_minutes("unknown") == 240
    print("incident_severity_sla: ok")
