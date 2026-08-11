"""Estimate affected user count from traffic share and total active users."""


def estimate_affected_users(total_active_users: int, traffic_share: float) -> int:
    if total_active_users <= 0:
        return 0
    return int(round(total_active_users * min(max(traffic_share, 0.0), 1.0)))


if __name__ == "__main__":
    assert estimate_affected_users(10000, 0.25) == 2500
    print("affected_users_estimator: ok")
