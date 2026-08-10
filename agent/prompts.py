SYSTEM_PROMPT = """
You are ChangeOps Commander, an autonomous incident-response agent for production services.

You may use tools: read_logs, get_metrics, git_recent_commits, git_show,
draft_rollback, draft_hotfix, run_shell, notify.

Rules:
1. Think step-by-step. Prefer small tool calls with clear purpose.
2. After each tool result, update your hypothesis in one sentence.
3. When you have a fix plan, call draft_rollback or draft_hotfix, then STOP
   and wait for human approval. Never call run_shell until approved.
4. After execution, verify with get_metrics and read_logs.
5. Prefer rollback of a bad deploy over clever hotfixes when uptime is at risk.
6. If evidence is weak, escalate instead of acting.
7. Hard cap: 12 tool calls, then escalate with a summary.
""".strip()

TOOL_SPECS = [
    {
        "name": "read_logs",
        "description": "Pull recent logs for a service.",
        "parameters": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "since_minutes": {"type": "integer", "default": 15},
                "level": {"type": "string", "enum": ["info", "warn", "error"]},
            },
            "required": ["service"],
        },
    },
    {
        "name": "get_metrics",
        "description": "Get error rate, latency, CPU for a service window.",
        "parameters": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "window_minutes": {"type": "integer", "default": 15},
            },
            "required": ["service"],
        },
    },
    {
        "name": "git_recent_commits",
        "description": "List recent commits for a repo/service.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "n": {"type": "integer", "default": 5},
            },
            "required": ["repo"],
        },
    },
    {
        "name": "git_show",
        "description": "Show diff and files for a commit sha.",
        "parameters": {
            "type": "object",
            "properties": {
                "repo": {"type": "string"},
                "sha": {"type": "string"},
            },
            "required": ["repo", "sha"],
        },
    },
    {
        "name": "draft_rollback",
        "description": "Draft a rollback proposal to a previous sha.",
        "parameters": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "to_sha": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["service", "to_sha", "reason"],
        },
    },
    {
        "name": "draft_hotfix",
        "description": "Draft a minimal hotfix proposal.",
        "parameters": {
            "type": "object",
            "properties": {
                "service": {"type": "string"},
                "reason": {"type": "string"},
                "notes": {"type": "string"},
            },
            "required": ["service", "reason"],
        },
    },
    {
        "name": "run_shell",
        "description": "Run a shell command. REQUIRES approval_id from a human-approved proposal.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "approval_id": {"type": "string"},
            },
            "required": ["command", "approval_id"],
        },
    },
    {
        "name": "notify",
        "description": "Notify humans on a channel.",
        "parameters": {
            "type": "object",
            "properties": {
                "channel": {"type": "string"},
                "message": {"type": "string"},
            },
            "required": ["channel", "message"],
        },
    },
]
