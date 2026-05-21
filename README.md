# Pulse

Pulse is a community intelligence platform for live-service games. It ingests player feedback from Reddit, classifies it with NLP, ranks problem areas by severity, and turns repeated complaints into tracked issues a dev team can act on.

The demo is configured around a football title, but the architecture works for any game with an active subreddit.

## Live demo

https://pulse-community.vercel.app

Sign in with `pulse_admin` / `pulse_admin`.

The deployment runs on seed data. Reddit ingestion is implemented and activates once API credentials are set.

## Architecture

Five backend services plus a web frontend:

- Gateway: JWT auth, rate limiting, routing, health checks (FastAPI)
- Ingestion: seed loading and Reddit ingestion (FastAPI)
- Processing: classification, sentiment, keywords, severity scoring (FastAPI)
- Analytics: trends, rankings, patch impact (Spring Boot)
- Issues: issue generation, lifecycle tracking, alerts (FastAPI)
- Frontend: React and TypeScript dashboard

Shared infra: PostgreSQL and Redis, orchestrated with Docker Compose.

The gateway is the only public entry point. Backend services run on the internal network and are never exposed directly.

## Tech Stack

Python, FastAPI, SQLAlchemy, Pydantic, Java, Spring Boot, PostgreSQL, Redis, React, TypeScript, Vite, Tailwind CSS, Docker Compose.

## Quick Start

```bash
git clone <repo-url>
cd pulse
cp .env.example .env
docker compose up --build
```

Frontend: `http://localhost:3000`
Gateway docs: `http://localhost:8000/docs`

Log in through `POST /api/auth/login` with the default credentials above, then authorize Swagger with `Bearer <token>`.

## Demo flow

```text
POST /api/ingest/seed
POST /api/process/batch
POST /api/issues/auto-generate
GET  /api/trends/overview
GET  /api/rankings
GET  /api/issues?page=1&page_size=5
```

## Deployment

Frontend on Vercel, built from `services/frontend`. Gateway, analytics, issues, and PostgreSQL on Fly.io. The gateway is the single public backend entry point, with CORS restricted to the deployed frontend.

## Testing

```powershell
.\scripts\smoke-test.ps1
.\scripts\smoke-test.ps1 -CheckNegativeCases
python -m pytest .\services\gateway\tests
```

See [docs/testing.md](docs/testing.md) and [docs/demo-walkthrough.md](docs/demo-walkthrough.md).

## Environment Variables

Backend variables are in `.env.example`. The frontend reads `VITE_API_BASE_URL` from `services/frontend/.env.example`. Reddit credentials are optional when using the seed dataset.

## Repo Structure

```text
pulse/
|-- data/
|-- docs/
|-- scripts/
|-- services/
|   |-- analytics/
|   |-- frontend/
|   |-- gateway/
|   |-- ingestion/
|   |-- issues/
|   `-- processing/
|-- docker-compose.yml
`-- README.md
```