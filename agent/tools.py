"""Tool adapters for ChangeOps Commander.

MVP behavior is dry-run / demo fixtures so the agent loop can be developed
without production credentials. Replace bodies with real integrations later.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ToolResult:
    ok: bool
    data: dict[str, Any]
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "data": self.data, "error": self.error, "ts": _now()}


# In-memory approval tokens granted by a human operator / API.
APPROVALS: set[str] = set()


def grant_approval(approval_id: str) -> None:
    APPROVALS.add(approval_id)


def read_logs(service: str, since_minutes: int = 15, level: str = "error") -> ToolResult:
    # Demo fixture matching the UI mock incident
    if service == "checkout-api":
        return ToolResult(
            ok=True,
            data={
                "lines": [
                    "14:02:01 ERROR TypeError: Cannot read properties of undefined (reading 'stripe_id') in payments/client.py:112",
                    "14:02:02 ERROR TypeError: Cannot read properties of undefined (reading 'stripe_id') in payments/client.py:112",
                    "14:02:03 ERROR payment_failed request_id=req_9f2",
                ],
                "error_count": 42,
                "since_minutes": since_minutes,
                "level": level,
            },
        )
    return ToolResult(ok=True, data={"lines": [], "error_count": 0})


def get_metrics(service: str, window_minutes: int = 15) -> ToolResult:
    if service == "checkout-api":
        return ToolResult(
            ok=True,
            data={"error_rate": 0.124, "p95_ms": 850, "cpu": 0.45, "window_minutes": window_minutes},
        )
    return ToolResult(ok=True, data={"error_rate": 0.001, "p95_ms": 120, "cpu": 0.2})


def git_recent_commits(repo: str, n: int = 5) -> ToolResult:
    return ToolResult(
        ok=True,
        data={
            "repo": repo,
            "commits": [
                {"sha": "a3f19c2", "author": "dev@acme.io", "message": "refactor payment timeout", "ts": "14:00:05"},
                {"sha": "b8e42a1", "author": "dev@acme.io", "message": "update deps", "ts": "09:15:00"},
                {"sha": "c11aa00", "author": "dev@acme.io", "message": "healthcheck tweak", "ts": "yesterday"},
            ][:n],
        },
    )


def git_show(repo: str, sha: str) -> ToolResult:
    return ToolResult(
        ok=True,
        data={
            "repo": repo,
            "sha": sha,
            "files": ["payments/client.py"],
            "diff": (
                "--- a/payments/client.py\n"
                "+++ b/payments/client.py\n"
                "@@ -110,7 +110,6 @@\n"
                "-    if customer is None:\n"
                "-        raise ValueError('missing customer')\n"
                "     stripe_id = customer.stripe_id\n"
            ),
        },
    )


def draft_rollback(service: str, to_sha: str, reason: str) -> ToolResult:
    proposal_id = f"prop_rb_{to_sha}"
    return ToolResult(
        ok=True,
        data={
            "proposal_id": proposal_id,
            "kind": "rollback",
            "service": service,
            "to_sha": to_sha,
            "reason": reason,
            "summary": f"Rollback {service} to {to_sha}: {reason}",
            "commands": [
                f"kubectl set image deployment/{service} {service}=registry/{service}:{to_sha}",
                f"kubectl rollout status deployment/{service}",
            ],
            "risk": "HIGH",
            "requires_approval": True,
        },
    )


def draft_hotfix(service: str, reason: str, notes: str = "") -> ToolResult:
    proposal_id = f"prop_hf_{service}"
    return ToolResult(
        ok=True,
        data={
            "proposal_id": proposal_id,
            "kind": "hotfix",
            "service": service,
            "reason": reason,
            "notes": notes,
            "summary": f"Hotfix {service}: {reason}",
            "commands": ["# apply patch via CI", f"kubectl rollout restart deployment/{service}"],
            "risk": "MEDIUM",
            "requires_approval": True,
        },
    )


def run_shell(command: str, approval_id: str) -> ToolResult:
    if approval_id not in APPROVALS:
        return ToolResult(ok=False, data={}, error="approval_required: missing or invalid approval_id")
    # Dry-run by default
    return ToolResult(
        ok=True,
        data={
            "command": command,
            "exit_code": 0,
            "stdout": f"[dry-run] would execute: {command}",
            "stderr": "",
            "mode": "dry_run",
        },
    )


def notify(channel: str, message: str) -> ToolResult:
    return ToolResult(ok=True, data={"channel": channel, "message": message, "delivered": True})


DISPATCH = {
    "read_logs": lambda **kw: read_logs(**kw),
    "get_metrics": lambda **kw: get_metrics(**kw),
    "git_recent_commits": lambda **kw: git_recent_commits(**kw),
    "git_show": lambda **kw: git_show(**kw),
    "draft_rollback": lambda **kw: draft_rollback(**kw),
    "draft_hotfix": lambda **kw: draft_hotfix(**kw),
    "run_shell": lambda **kw: run_shell(**kw),
    "notify": lambda **kw: notify(**kw),
}


def call_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    if name not in DISPATCH:
        return ToolResult(ok=False, data={}, error=f"unknown_tool:{name}").as_dict()
    try:
        return DISPATCH[name](**args).as_dict()
    except TypeError as e:
        return ToolResult(ok=False, data={}, error=f"bad_args:{e}").as_dict()
