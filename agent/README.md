# Agent scaffold

Python runtime stub for ChangeOps Commander.

This is **not** wired to the UI yet. The dashboard runs on mock data.
During the CodeSplash build week, replace the stubs with real tool adapters
and an OpenAI-compatible client pointed at Ollama / vLLM (Llama 3.1, Mistral, etc.).

## Planned run

```bash
cd agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_BASE_URL=http://localhost:11434/v1
export OPENAI_API_KEY=ollama
export OPENAI_MODEL=llama3.1
python main.py --demo
```

## Files

- `main.py` — incident loop + approval gate
- `tools.py` — tool implementations (dry-run by default)
- `prompts.py` — system prompt + tool specs
