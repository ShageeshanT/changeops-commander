"""Allowlist of automated actions considered safe to auto-approve."""

SAFE_ACTIONS = {"clear_cache", "restart_worker", "scale_up_replica", "rotate_log_file"}


def is_safe_action(action_name: str) -> bool:
    return action_name in SAFE_ACTIONS


if __name__ == "__main__":
    assert is_safe_action("clear_cache") is True
    assert is_safe_action("delete_database") is False
    print("safe_action_allowlist: ok")
