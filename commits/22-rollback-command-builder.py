"""Build a safe rollback command string from a deploy record."""


def build_rollback_command(service: str, target_version: str, dry_run: bool = True) -> str:
    base = f"deploy rollback --service {service} --version {target_version}"
    return f"{base} --dry-run" if dry_run else base


if __name__ == "__main__":
    cmd = build_rollback_command("api", "1.4.2")
    assert "--dry-run" in cmd
    print("rollback_command_builder: ok")
