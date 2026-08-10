const mockIncidentEvents = [
  {
    ts: "14:02:10",
    kind: "observe",
    title: "Alert Triggered",
    detail: "checkout-api error rate > 5% (current: 12.4%)"
  },
  {
    ts: "14:02:12",
    kind: "tool",
    title: "Tool Call: get_metrics",
    detail: "Checking checkout-api metrics for the last 15m",
    code: '{"service": "checkout-api", "window": 15}\n\nResult: { "error_rate": 0.124, "p95_ms": 850, "cpu": 0.45 }'
  },
  {
    ts: "14:02:15",
    kind: "tool",
    title: "Tool Call: read_logs",
    detail: "Pulling recent error logs for checkout-api",
    code: '{"service": "checkout-api", "level": "error", "since": 5}\n\nResult: 42x "TypeError: Cannot read properties of undefined (reading \'stripe_id\') in payments/client.py:112"'
  },
  {
    ts: "14:02:18",
    kind: "tool",
    title: "Tool Call: git_recent_commits",
    detail: "Checking recent deploys to checkout-api",
    code: '{"repo": "checkout-api", "n": 3}\n\nResult: [\n  { "sha": "a3f19c2", "msg": "refactor payment timeout", "ts": "14:00:05" },\n  { "sha": "b8e42a1", "msg": "update deps", "ts": "09:15:00" }\n]'
  },
  {
    ts: "14:02:22",
    kind: "tool",
    title: "Tool Call: git_show",
    detail: "Inspecting commit a3f19c2",
    code: '{"repo": "checkout-api", "sha": "a3f19c2"}\n\nResult: diff shows changes to payments/client.py line 112 removing null check on customer object.'
  },
  {
    ts: "14:02:25",
    kind: "propose",
    title: "Diagnosis & Proposal",
    detail: "Commit a3f19c2 introduced a regression in payments/client.py causing 500s. Proposing rollback to b8e42a1.",
    proposal: {
      summary: "Rollback checkout-api to b8e42a1 to mitigate TypeError in payments/client.py",
      commands: "kubectl set image deployment/checkout-api checkout-api=registry/checkout-api:b8e42a1\nkubectl rollout status deployment/checkout-api",
      risk: "HIGH - Mutating production state"
    }
  }
];

const mockExecutionEvents = [
  {
    ts: "14:03:10",
    kind: "execute",
    title: "Tool Call: run_shell (APPROVED)",
    detail: "Executing rollback commands",
    code: 'Exit code: 0\nstdout: deployment.apps/checkout-api image updated\ndeployment "checkout-api" successfully rolled out'
  },
  {
    ts: "14:03:45",
    kind: "tool",
    title: "Tool Call: get_metrics",
    detail: "Verifying recovery",
    code: '{"service": "checkout-api", "window": 2}\n\nResult: { "error_rate": 0.001, "p95_ms": 120, "cpu": 0.30 }'
  },
  {
    ts: "14:03:50",
    kind: "observe",
    title: "Incident Resolved",
    detail: "Error rate returned to normal. Rollback successful."
  }
];
