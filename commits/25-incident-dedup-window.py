"""Sliding time window deduplication for repeated incident triggers."""


class DedupWindow:
    def __init__(self, window_seconds=900):
        self.window_seconds = window_seconds
        self._last_seen = {}

    def should_trigger(self, key: str, timestamp: float) -> bool:
        last = self._last_seen.get(key)
        if last is None or (timestamp - last) > self.window_seconds:
            self._last_seen[key] = timestamp
            return True
        return False


if __name__ == "__main__":
    w = DedupWindow(window_seconds=300)
    assert w.should_trigger("db-down", 0) is True
    assert w.should_trigger("db-down", 100) is False
    assert w.should_trigger("db-down", 400) is True
    print("incident_dedup_window: ok")
