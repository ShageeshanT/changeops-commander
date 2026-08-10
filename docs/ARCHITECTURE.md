# Architecture

## Overview

ChangeOps Commander is split into three layers:

```
┌─────────────────────────────────────────────────────────┐
│  UI (static dashboard)                                  │
│  incident feed · agent timeline · approval gate · audit │
└──────────────────────────▲──────────────────────────────┘
                           │ REST / SSE (future)
┌──────────────────────────┴──────────────────────────────┐
│  Agent runtime (Python)                                 │
│  planner · tool router · approval broker · verifier     │
└──────▲──────────────▲──────────────▲────────────────────┘
       │              │              │
   logs/metrics     git/scm        shell/deploy
   adapters         adapters       adapters (gated)
```

## Components

### 1. Dashboard (this MVP)

- Pure HTML/CSS/JS, no framework required for the demo.
- Consumes either:
  - **Mock bus** (`ui/mock-data.js` + `app.js` simulator), or later
  - **Live API** (`GET /incidents`, `GET /incidents/:id/events`, `POST /approvals`).
- Renders:
  - Service health strip
  - Incident list
  - Agent reasoning + tool-call timeline
  - Proposed action card with Approve / Reject
  - Immutable audit log

### 2. Agent runtime (scaffold)

Language: Python 3.11+

Responsibilities:

- Maintain incident state machine (see `AGENT_SPEC.md`)
- Call tools with structured arguments
- Persist every observation / thought / action
- Block on `AWAIT_APPROVAL` before any mutating tool
- Verify post-execution health and close or escalate

Model interface: OpenAI-compatible chat completions so Ollama, vLLM, llama.cpp, and Together-hosted open models all work the same way.

### 3. Tool adapters

Each tool is a small module with:

- JSON schema (for the model)
- `dry_run` path
- `execute` path
- structured result + error type

Mutating adapters share a common `ApprovalToken` check.

## Data model (simplified)

```text
Incident {
  id, service, severity, status,
  opened_at, closed_at?,
  summary, root_cause?,
  events: Event[],
  proposal?: Proposal,
  audit: AuditEntry[]
}

Event {
  ts, kind: observe|think|tool|propose|approve|execute|verify|error,
  title, detail, tool?, args?, result?
}

Proposal {
  id, kind: rollback|hotfix|scale|config,
  summary, risk, commands[], requires_approval: true
}
```

## Deployment targets

| Stage | UI | Agent | Model |
|-------|----|-------|-------|
| Local demo | `python -m http.server` | mock in browser | n/a |
| Dev | static + FastAPI | Python runtime | Ollama Llama 3.1 |
| Hackathon demo | Vercel/Netlify static | Railway/Fly API | hosted open model or Ollama tunnel |
| Production sketch | CDN | k8s job + queue | private vLLM |

## Security boundaries

1. UI never holds deploy credentials.
2. Agent service holds short-lived tokens only.
3. Mutating tools require an approval id signed by the API.
4. Audit log is append-only (file or SQLite in MVP).
5. Network egress allow-list for tool hosts.

## Observability

- Structured JSON logs from the agent
- Per-incident event stream (SSE)
- Simple metrics: MTTD, MTTR, approval latency, tool error rate

## Non-goals (MVP)

- Full multi-cluster orchestration
- Automatic production deploys without approval
- Training custom models
- Mobile native apps
