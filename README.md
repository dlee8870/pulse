# Pulse

Pulse is a community intelligence platform for live-service games. It ingests player reviews from Steam, classifies them with NLP, ranks problem areas by severity, and turns repeated complaints into tracked issues a dev team can act on.

The demo is configured around EA SPORTS FC 26, but the architecture works for any game with Steam reviews.

## Live demo

https://pulse-community.vercel.app

Sign in with `pulse_admin` / `pulse_admin`.

The deployment runs on real EA SPORTS FC 26 reviews pulled from Steam's public reviews endpoint. No API key is required for ingestion.

## Architecture

Five backend services plus a web frontend:

- Gateway: JWT auth, rate limiting, routing, health checks (FastAPI)
- Ingestion: Steam review ingestion and seed loading (FastAPI)
- Processing: classification, sentiment, keywords, severity scoring (FastAPI)
- Analytics: trends, rankings, patch impact (Spring Boot)
- Issues: issue generation, lifecycle tracking, alerts (FastAPI)
- Frontend: React and TypeScript dashboard

Shared infra: PostgreSQL and Redis, orchestrated with Docker Compose.

The gateway is the only public entry point. Backend services run on the internal network and are never exposed directly.

## How classification works

Each review runs through a two-model pipeline:

- Category is assigned by zero-shot classification with `facebook/bart-large-mnli`. The model scores the review against plain-language category descriptions, so it reads meaning rather than matching strings, and handles negation and unseen phrasing. A confidence floor files low-confidence reviews under `other` instead of guessing.
- Subcategory is picked by keyword rules within the winning category only, where precise vocabulary matching is reliable. The original keyword-only classifier is kept in the repo as the v1 approach.
- Sentiment is scored with `cardiffnlp/twitter-roberta-base-sentiment-latest`. Steam censors profanity as runs of heart characters, which the model would otherwise read as affection, so input text is normalized before scoring. Stored review text is unchanged.
- The two models cross-check each other: a review classified as praise but scored negative by the sentiment model is reclassified with the praise label excluded, which catches sarcasm.
- Severity blends sentiment intensity, a category weight, and engagement.

Known limitation: each review gets exactly one category, so a review complaining about several things is filed under its dominant theme. Multi-label classification is the planned next step.

## Tech Stack

Python, FastAPI, SQLAlchemy, Pydantic, HuggingFace Transformers, Java, Spring Boot, PostgreSQL, Redis, React, TypeScript, Vite, Tailwind CSS, Docker Compose.

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
POST /api/ingest/steam
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

Backend variables are in `.env.example`. The frontend reads `VITE_API_BASE_URL` from `services/frontend/.env.example`. Steam ingestion needs no credentials. Reddit credentials are optional and only used by the legacy Reddit endpoint.

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