"""Check whether a change freeze window is currently active."""

from datetime import datetime


def is_freeze_active(freeze_windows, now=None):
    """freeze_windows: list of (start_datetime, end_datetime)."""
    now = now or datetime.utcnow()
    for start, end in freeze_windows:
        if start <= now <= end:
            return True
    return False


if __name__ == "__main__":
    windows = [(datetime(2026, 12, 20), datetime(2027, 1, 2))]
    assert is_freeze_active(windows, datetime(2026, 12, 25)) is True
    assert is_freeze_active(windows, datetime(2026, 8, 11)) is False
    print("change_freeze_checker: ok")
