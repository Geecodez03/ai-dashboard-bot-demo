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
