# AI Dashboard Bot Demo

Live demo: https://ai-dashboard-bot-demo.onrender.com

## What this shows employers
- Build + deploy a full-stack demo (frontend + API) that returns dashboard-ready JSON
- AI integration with safe fallbacks (demo mode when no key is present)
- Automation workflow logic + audit/history logging

## Endpoints
- GET /health
- GET /api/info
- POST /api/ask
- POST /api/workflow/demo
- GET /api/history?limit=10

## Quick tests (PowerShell)

```powershell
$u="https://ai-dashboard-bot-demo.onrender.com"
Invoke-RestMethod "$u/health"
Invoke-RestMethod "$u/api/info"
Invoke-RestMethod -Method Post -Uri "$u/api/ask" -ContentType "application/json" -Body '{"question":"Give 3 bullets explaining this demo."}'
```

## First-time local setup (PowerShell)

```powershell
python -m venv .venv-local
.\.venv-local\Scripts\Activate.ps1
pip install -r backend/requirements.txt
python -m pytest backend/tests -q
```

## Local setup notes
- Create and use a local virtual environment for development only.
- Keep environment and cache artifacts out of git (`backend/.venv/`, `.venv-local/`, `__pycache__/`, `.pytest_cache/`).
- If these were ever tracked, remove them from index only with `git rm -r --cached <path>`.
- Keep local SQLite files untracked (`data.db`, `backend/data.db`).
