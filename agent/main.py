"""ChangeOps Commander — agent loop scaffold.

This demo path does not call a live LLM. It walks a scripted ReAct-style
trace using the tool adapters so the event schema matches the UI.

Wire an OpenAI-compatible client (Ollama/vLLM + Llama 3.1) in place of
`scripted_plan()` for the real agentic core.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from typing import Any

from prompts import SYSTEM_PROMPT
from tools import call_tool, grant_approval


@dataclass
class Event:
    kind: str
    title: str
    detail: str
    tool: str | None = None
    args: dict[str, Any] | None = None
    result: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "title": self.title,
            "detail": self.detail,
            "tool": self.tool,
            "args": self.args,
            "result": self.result,
        }


@dataclass
class Incident:
    id: str
    service: str
    severity: str = "SEV-2"
    status: str = "TRIAGING"
    events: list[Event] = field(default_factory=list)
    proposal: dict[str, Any] | None = None

    def log(self, event: Event) -> None:
        self.events.append(event)
        print(f"[{event.kind}] {event.title} — {event.detail}")


def scripted_plan(incident: Incident) -> None:
    """Deterministic demo of the agentic loop (replace with LLM tool-calling)."""
    incident.log(Event("observe", "Alert received", f"{incident.service} error rate spike"))

    steps = [
        ("get_metrics", {"service": incident.service, "window_minutes": 15}, "Pull live metrics"),
        ("read_logs", {"service": incident.service, "since_minutes": 5, "level": "error"}, "Read recent errors"),
        ("git_recent_commits", {"repo": incident.service, "n": 3}, "Inspect recent deploys"),
        ("git_show", {"repo": incident.service, "sha": "a3f19c2"}, "Inspect suspect commit"),
        (
            "draft_rollback",
            {
                "service": incident.service,
                "to_sha": "b8e42a1",
                "reason": "a3f19c2 removed null check; stripe_id TypeError burst",
            },
            "Draft rollback proposal",
        ),
    ]

    for tool, args, why in steps:
        incident.log(Event("think", "Planning next action", why))
        result = call_tool(tool, args)
        incident.log(
            Event(
                "tool",
                f"Tool: {tool}",
                why,
                tool=tool,
                args=args,
                result=result,
            )
        )
        if tool.startswith("draft_") and result.get("ok"):
            incident.proposal = result["data"]
            incident.status = "AWAIT_APPROVAL"
            incident.log(
                Event(
                    "propose",
                    "Awaiting human approval",
                    incident.proposal.get("summary", ""),
                )
            )


def approve_and_execute(incident: Incident, approval_id: str | None = None) -> None:
    if not incident.proposal:
        raise RuntimeError("no proposal to approve")
    approval_id = approval_id or incident.proposal["proposal_id"]
    grant_approval(approval_id)
    incident.status = "EXECUTING"

    for cmd in incident.proposal.get("commands", []):
        result = call_tool("run_shell", {"command": cmd, "approval_id": approval_id})
        incident.log(
            Event(
                "execute",
                "Gated shell execution",
                cmd,
                tool="run_shell",
                args={"command": cmd, "approval_id": approval_id},
                result=result,
            )
        )

    verify = call_tool("get_metrics", {"service": incident.service, "window_minutes": 2})
    incident.log(
        Event(
            "verify",
            "Post-fix verification",
            "Checking error rate after rollback",
            tool="get_metrics",
            result=verify,
        )
    )
    incident.status = "RESOLVED"
    incident.log(Event("observe", "Incident resolved", "Metrics recovered; closing incident"))


def main() -> None:
    parser = argparse.ArgumentParser(description="ChangeOps Commander agent scaffold")
    parser.add_argument("--demo", action="store_true", help="Run scripted incident demo")
    parser.add_argument("--approve", action="store_true", help="Auto-approve proposal in demo")
    parser.add_argument("--json-out", type=str, default="", help="Write event trace JSON to path")
    args = parser.parse_args()

    print("System prompt loaded (first 120 chars):", SYSTEM_PROMPT[:120], "...")

    if not args.demo:
        print("No live model wired yet. Re-run with --demo for the scripted loop.")
        return

    incident = Incident(id="inc_demo_1", service="checkout-api")
    scripted_plan(incident)

    if args.approve and incident.proposal:
        approve_and_execute(incident)

    payload = {
        "incident": {
            "id": incident.id,
            "service": incident.service,
            "severity": incident.severity,
            "status": incident.status,
            "proposal": incident.proposal,
            "events": [e.as_dict() for e in incident.events],
        }
    }

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        print(f"Wrote trace to {args.json_out}")
    else:
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
