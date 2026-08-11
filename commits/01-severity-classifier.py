"""Classify incident severity from live signal counts and error rate."""


def classify_severity(active_alerts: int, error_rate: float, affected_services: int) -> str:
    """Return SEV1-SEV4 based on simple weighted thresholds."""
    if error_rate >= 0.25 or affected_services >= 5:
        return "SEV1"
    if error_rate >= 0.10 or affected_services >= 3 or active_alerts >= 10:
        return "SEV2"
    if error_rate >= 0.02 or active_alerts >= 3:
        return "SEV3"
    return "SEV4"


if __name__ == "__main__":
    assert classify_severity(1, 0.30, 1) == "SEV1"
    assert classify_severity(2, 0.01, 1) == "SEV4"
    print("severity_classifier: ok")
