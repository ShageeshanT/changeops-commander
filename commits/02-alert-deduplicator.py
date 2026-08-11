"""Deduplicate alerts by fingerprint within a rolling time window."""


def dedupe_alerts(alerts, window_seconds=300):
    """alerts: list of (fingerprint, timestamp). Returns unique alerts kept."""
    seen = {}
    kept = []
    for fingerprint, ts in sorted(alerts, key=lambda a: a[1]):
        last = seen.get(fingerprint)
        if last is None or ts - last > window_seconds:
            kept.append((fingerprint, ts))
            seen[fingerprint] = ts
    return kept


if __name__ == "__main__":
    result = dedupe_alerts([("db-timeout", 0), ("db-timeout", 100), ("db-timeout", 400)])
    assert len(result) == 2
    print("alert_deduplicator: ok")
