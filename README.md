# Wiredware

AI-powered security gate for git. It checks every push against a set of security advisory PDFs using embeddings and an LLM, and blocks commits that introduce known vulnerability patterns.

## How it works

1. Security advisory PDFs live in `security_reports/`.
2. On each check, the code diff is converted to an embedding and compared against the report embeddings to find the most relevant advisory.
3. The diff and the matched report are sent to a local LLM (Ollama, `qwen3.5:4b`) which decides if the code is vulnerable.
4. If vulnerable — the push is blocked. Otherwise it goes through.

## Requirements

- Python 3.12+
- [Ollama](https://ollama.com) running locally with `qwen3.5:4b` pulled
- Python packages: `fastapi`, `uvicorn`, `ollama`, `pymupdf`, `fastembed`, `rich`

```
pip install fastapi uvicorn ollama pymupdf fastembed rich
```

## Git hook (standalone mode)

The hook runs the check directly in your git workflow. On `git push`, it diffs against upstream, runs the security check, and exits non-zero to block the push if a vulnerability is found.

### Install the hook

Linux / macOS:
```bash
cat << 'EOF' > .git/hooks/pre-push
#!/usr/bin/env bash
cd "$(git rev-parse --show-toplevel)/src"
python git_hook.py
EOF
chmod +x .git/hooks/pre-push
```

Windows (PowerShell):
```powershell
@"
#!/usr/bin/env bash
cd "`$(git rev-parse --show-toplevel)/src"
python git_hook.py
"@ | Set-Content -Path .git/hooks/pre-push -Encoding utf8
```

## Server mode (with dashboard)

The server wraps the same logic into an HTTP API and adds a web dashboard for monitoring scan results.

### Start the server

```
cd src
python serverlogic.py
```

This starts at `http://127.0.0.1:8000`. Open it in a browser to see the dashboard.

### API

**POST /check** — run a security check on a code snippet.

```json
{
  "code": "diff or code string here",
  "commit": "abc1234",
  "author": "John Doe"
}
```

`commit` and `author` are optional — they just show up in the dashboard table.

Response:
```json
{
  "report": "Security Advisory — SQL Injection in User Lookup.pdf",
  "vulnerable": true,
  "reason": "The code concatenates user input directly into the SQL query.",
  "similarity": 0.54
}
```

**GET /reports** — list loaded advisory PDFs.

**GET /audit** — recent scan history as JSON.

**GET /health** — server status.

**GET /docs** — auto-generated API docs (Swagger UI).

## Project structure

```
wiredware/
  security_reports/     PDF advisories to check against
  src/
    base_logic.py       Embedding, comparison, PDF parsing
    git_logic.py        LLM call and git diff retrieval
    git_hook.py         Standalone pre-push hook
    serverlogic.py      HTTP server + dashboard
```
