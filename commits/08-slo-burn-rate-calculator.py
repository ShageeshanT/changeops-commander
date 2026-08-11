"""Calculate SLO error budget burn rate from error and total request counts."""


def burn_rate(error_count: int, total_count: int, slo_target: float = 0.999) -> float:
    if total_count <= 0:
        return 0.0
    error_budget = 1 - slo_target
    actual_error_rate = error_count / total_count
    if error_budget <= 0:
        return float("inf")
    return round(actual_error_rate / error_budget, 3)


if __name__ == "__main__":
    rate = burn_rate(10, 1000)
    assert rate > 1
    print("slo_burn_rate_calculator: ok")
