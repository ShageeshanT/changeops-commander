# Demo guide

## 60-second pitch

> “When a deploy breaks production, ChangeOps Commander does the on-call work: it reads the alert, pulls logs, blames the right commit, drafts a rollback, and waits for one human click before it executes. Fully agentic. Open-source model ready. Human still owns the blast radius.”

## 3-minute walkthrough

### Setup

```bash
cd changeops-commander
python3 -m http.server 8080
```

Open `http://localhost:8080`.

### Flow

1. **Healthy state** — green services on the top strip.  
2. Hit **Simulate incident**.  
3. Point at the **Agent timeline**:
   - Observe alert (error rate spike on `checkout-api`)
   - `read_logs` → burst of 500s after 14:02
   - `git_recent_commits` → deploy `a3f19c2` “refactor payment timeout”
   - `git_show` → risky change in `payments/client.py`
   - Diagnosis: bad deploy
   - `draft_rollback` to previous sha
4. **Proposal card** appears with risk + commands.  
5. Click **Approve & execute**.  
6. Timeline shows gated `run_shell`, then verify metrics recovering.  
7. Incident moves to **Resolved**; audit log has every step.

### Talking points for judges

- Multi-step tool use, not a single LLM answer  
- Explicit approval boundary (safety)  
- Works with local Llama/Mistral (see ARCHITECTURE + AGENT_SPEC)  
- UI is real; agent core is specified and scaffolded for the build week  

## Backup if live agent is not ready

The UI simulator is enough for proposal review and early demos. Say clearly:

> “Today’s demo is the product surface and the agent contract. During the mentorship week we wire Llama 3.1 via Ollama to the same event schema you see here.”
