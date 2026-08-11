"""Match an incident type to the best runbook by tag overlap."""


def match_runbook(incident_tags, runbooks):
    """runbooks: list of dicts with 'name' and 'tags'. Returns best match name or None."""
    best_name = None
    best_score = 0
    incident_set = set(incident_tags)
    for rb in runbooks:
        overlap = len(incident_set & set(rb.get("tags", [])))
        if overlap > best_score:
            best_score = overlap
            best_name = rb.get("name")
    return best_name


if __name__ == "__main__":
    rbs = [{"name": "db-failover", "tags": ["database", "timeout"]}, {"name": "cdn-purge", "tags": ["cdn"]}]
    assert match_runbook(["database", "timeout"], rbs) == "db-failover"
    print("runbook_matcher: ok")
