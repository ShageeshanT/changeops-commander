# Roadmap

## Phase 0 — UI MVP (done)

- [x] Dashboard shell
- [x] Mock incident + agent timeline
- [x] Approval gate UX
- [x] Architecture / agent / demo docs
- [x] Python agent scaffold stubs

## Phase 1 — Proposal polish (before Aug 21)

- [ ] One-page proposal PDF from these docs
- [ ] 60s screen recording of the UI demo
- [ ] Team roles + open-source model choice locked (Llama 3.1 default)
- [ ] Repo public with clean README

## Phase 2 — Mentorship / build week (Sep 4–10)

- [ ] FastAPI event API matching UI schema
- [ ] Ollama tool-calling ReAct loop
- [ ] Real `read_logs` from sample log files
- [ ] Real `git_*` tools against a demo repo
- [ ] Approval token wiring to `run_shell` dry-run + real
- [ ] SSE stream into the dashboard (replace mock)

## Phase 3 — Stretch

- [ ] Slack / WhatsApp notify tool
- [ ] Multi-service correlation
- [ ] MTTD/MTTR dashboard charts
- [ ] Policy engine (which services allow auto-rollback)

## Explicit non-goals before finale

- Training a custom model
- Full Kubernetes operator
- Replacing a commercial observability suite
