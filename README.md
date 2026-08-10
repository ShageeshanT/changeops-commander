# ChangeOps Commander

**Agentic infrastructure incident response for the CodeSplash Agentic AI Phase.**

ChangeOps Commander is an autonomous agent that watches service health, diagnoses incidents from logs + git history, proposes a fix or rollback, and only executes after human approval.

> UI-first MVP. The dashboard is fully documented and runnable. Live agent backends are stubbed with realistic mock data so judges can walk the full incident flow without cloud credentials.

---

## Problem

When a deploy breaks production, humans still do the slow loop:

1. Notice the alert  
2. Dig through logs  
3. Blame the last commit  
4. Write a rollback / hotfix  
5. Get approval  
6. Execute  

Minutes of downtime become hours. ChangeOps Commander collapses steps 1–4 into an agentic plan and keeps a human in the loop for step 5–6.

---

## What this MVP shows

| Surface | Status |
|--------|--------|
| Dark ops dashboard UI | Done |
| Live incident feed (mock) | Done |
| Agent reasoning timeline | Done |
| Tool-call trace (logs, git, shell) | Done |
| Fix proposal + approval gate | Done |
| Architecture & agent design docs | Done |
| Real LLM / GitHub / shell adapters | Scaffolded stubs |

---

## Quick start (UI)

```bash
# no build step — static UI
cd changeops-commander
python3 -m http.server 8080
# open http://localhost:8080
```

Or open `index.html` directly in a browser.

---

## Demo script (for judges)

1. Open the dashboard.  
2. Click **Simulate incident** (or wait for the auto demo pulse).  
3. Watch the agent:
   - pull metrics / alert
   - read recent logs
   - inspect last 5 commits
   - draft a rollback plan
4. Review the proposed action card.  
5. Click **Approve & execute** or **Reject**.  
6. See the audit trail update.

---

## Agentic design (CodeSplash-ready)

### Goal

Autonomous multi-step incident response with tool use, planning, and a hard human approval boundary.

### Open-source model requirement

For the scored agentic core, run a local / self-hosted open model (e.g. Llama 3.1 8B/70B, Mistral, Qwen2.5) behind an OpenAI-compatible endpoint. Proprietary APIs may assist the UI demo but **must not** be the scored agent brain.

Suggested local stack:

- **Ollama** or **vLLM** serving `llama3.1:8b-instruct` (dev) / larger for demos  
- **LangGraph** or plain ReAct loop in Python  
- Tools as plain functions with JSON schemas  

### Agent loop

```
observe → plan → tool_call* → diagnose → propose_fix → AWAIT_APPROVAL → execute → verify → report
```

### Tools (planned)

| Tool | Purpose |
|------|---------|
| `read_logs(service, since, level)` | Pull structured / text logs |
| `get_metrics(service, window)` | CPU, error rate, latency |
| `git_recent_commits(repo, n)` | What changed recently |
| `git_show(sha)` | Inspect a commit diff |
| `draft_rollback(service, to_sha)` | Produce rollback plan |
| `draft_hotfix(path, patch)` | Produce a minimal patch |
| `run_shell(cmd)` | Gated execution (approval required) |
| `notify(channel, message)` | Slack / WhatsApp / email |

### Safety

- Destructive tools (`run_shell`, deploy, rollback apply) require explicit human approval.  
- Panic stop kills in-flight execution.  
- Full audit log of every tool call + decision.  
- Least-privilege credentials; dry-run mode by default.

---

## Repository layout

```
changeops-commander/
├── README.md                 # this file
├── docs/
│   ├── ARCHITECTURE.md       # system design
│   ├── AGENT_SPEC.md         # agent prompts, tools, state machine
│   ├── DEMO.md               # judge walkthrough
│   └── ROADMAP.md            # path to full agent
├── ui/
│   ├── index.html            # dashboard shell
│   ├── styles.css
│   ├── app.js                # UI + mock agent simulation
│   └── mock-data.js
├── agent/                    # Python scaffold (not wired in UI MVP)
│   ├── README.md
│   ├── main.py
│   ├── tools.py
│   └── prompts.py
└── assets/
    └── favicon.svg
```

Note: the live UI is also served from the repo root (`index.html`) for one-click demos.

---

## Why this is a strong CodeSplash entry

1. **Clearly agentic** — multi-tool, multi-step, not a chatbot FAQ.  
2. **Real operational value** — DevOps / SRE pain everyone understands.  
3. **Open-source friendly** — works with local Llama/Mistral; no paid API required for the core loop.  
4. **Human-in-the-loop** — safety story judges care about.  
5. **Demoable in 3 minutes** — UI shows the full loop even before the backend is finished.

---

## Team notes

- Hackathon: CodeSplash Agentic AI Phase  
- Proposal window: Aug 9–21, 2026  
- Development window (if selected): Sep 4–10, 2026  
- Model constraint: open-source / non-proprietary for agentic scoring  

---

## License

MIT — see `LICENSE`.
