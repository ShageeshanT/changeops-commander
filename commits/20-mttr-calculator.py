"""Calculate mean time to resolution across resolved incidents."""


def calculate_mttr(incidents):
    """incidents: list of (detected_at, resolved_at) in seconds since epoch."""
    durations = [resolved - detected for detected, resolved in incidents if resolved > detected]
    if not durations:
        return 0.0
    return round(sum(durations) / len(durations), 2)


if __name__ == "__main__":
    mttr = calculate_mttr([(0, 600), (0, 1200)])
    assert mttr == 900.0
    print("mttr_calculator: ok")
