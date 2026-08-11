"""Filter out flapping alerts that fire and clear repeatedly in a short window."""


def filter_flapping(alert_events, flap_threshold=3, window_seconds=600):
    """alert_events: list of (fingerprint, timestamp, state) where state is 'firing'/'resolved'."""
    counts = {}
    for fingerprint, ts, state in alert_events:
        counts.setdefault(fingerprint, []).append(ts)

    flapping = set()
    for fingerprint, timestamps in counts.items():
        timestamps.sort()
        if len(timestamps) >= flap_threshold and (timestamps[-1] - timestamps[0]) <= window_seconds:
            flapping.add(fingerprint)
    return [e for e in alert_events if e[0] not in flapping]


if __name__ == "__main__":
    events = [("cpu-high", 0, "firing"), ("cpu-high", 60, "resolved"), ("cpu-high", 120, "firing")]
    result = filter_flapping(events, flap_threshold=3, window_seconds=600)
    assert result == []
    print("alert_noise_filter: ok")
