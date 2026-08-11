"""Priority queue that orders incidents by severity then age."""

import heapq

SEVERITY_RANK = {"SEV1": 0, "SEV2": 1, "SEV3": 2, "SEV4": 3}


class IncidentQueue:
    def __init__(self):
        self._heap = []
        self._counter = 0

    def push(self, incident_id: str, severity: str, created_at: float):
        rank = SEVERITY_RANK.get(severity, 9)
        heapq.heappush(self._heap, (rank, created_at, self._counter, incident_id))
        self._counter += 1

    def pop(self):
        if not self._heap:
            return None
        return heapq.heappop(self._heap)[3]


if __name__ == "__main__":
    q = IncidentQueue()
    q.push("INC-2", "SEV3", 10)
    q.push("INC-1", "SEV1", 20)
    assert q.pop() == "INC-1"
    print("incident_priority_queue: ok")
