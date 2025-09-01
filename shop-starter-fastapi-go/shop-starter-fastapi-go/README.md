# Shop Starter (FastAPI + Go)

A minimal monorepo to sell ready-made items (e.g., kitchen towels) and support custom **magnetic curtains** with dynamic pricing.

## Structure
- `backend/` — FastAPI API + simple HTML (Jinja2) for a quick UI.
- `go-pricer/` — Go microservice that calculates custom curtain prices.
- `frontend/` — Static assets and templates (served by FastAPI).

## Quick Start

### 1) Python backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Open: http://localhost:8000 and API docs http://localhost:8000/docs

### 2) Go pricer
```bash
cd go-pricer
go run main.go
```
Runs on http://localhost:8080

### 3) Seed some sample data (optional)
Use the interactive docs at http://localhost:8000/docs to POST products or extend models.
Ready-made curtain variants can be added directly in the SQLite DB or via a future admin route.

## Pricing
- Defaults (overridable via env):
  - `PVC_RATE_PER_SQM=25` AZN
  - `MESH_RATE_PER_SQM=15` AZN
  - `MAGNET_UNIT_PRICE=0.30` AZN
- Magnet count = perimeter(cm) / spacing(cm), spacing default **10cm** (configurable via request).

## Next Steps
- Add authentication and an admin panel.
- Add orders & checkout (e.g., Stripe).
- Replace HTML with a React/Next.js frontend when ready.
- Dockerize services for deployment.
