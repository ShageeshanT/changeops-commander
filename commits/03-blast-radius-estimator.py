"""Estimate blast radius from affected service count and traffic share."""


def estimate_blast_radius(affected_services: int, total_services: int, traffic_share: float) -> float:
    """Returns a 0-1 score combining service spread and traffic impact."""
    if total_services <= 0:
        return 0.0
    service_ratio = min(affected_services / total_services, 1.0)
    return round((service_ratio * 0.6) + (min(traffic_share, 1.0) * 0.4), 3)


if __name__ == "__main__":
    score = estimate_blast_radius(2, 10, 0.5)
    assert 0 <= score <= 1
    print("blast_radius_estimator: ok")
