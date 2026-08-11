"""Check whether a proposed automated action requires human approval."""

SENSITIVE_ACTIONS = {"delete_database", "force_deploy", "restart_prod_cluster", "revoke_access"}


def requires_approval(action_name: str, blast_radius: float = 0.0) -> bool:
    if action_name in SENSITIVE_ACTIONS:
        return True
    return blast_radius >= 0.5


if __name__ == "__main__":
    assert requires_approval("delete_database", 0.0) is True
    assert requires_approval("clear_cache", 0.1) is False
    print("approval_gate_checker: ok")
