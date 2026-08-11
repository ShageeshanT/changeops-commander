"""Simple z-score based anomaly detector for a metric series."""

import statistics


def detect_anomalies(series, z_threshold=2.0):
    if len(series) < 2:
        return []
    mean = statistics.mean(series)
    stdev = statistics.pstdev(series) or 1e-9
    anomalies = []
    for i, value in enumerate(series):
        z = (value - mean) / stdev
        if abs(z) >= z_threshold:
            anomalies.append(i)
    return anomalies


if __name__ == "__main__":
    series = [10, 11, 9, 10, 12, 500]
    assert 5 in detect_anomalies(series, z_threshold=2.0)
    print("metric_anomaly_detector: ok")
