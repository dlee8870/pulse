# Pulse

Pulse is a community intelligence platform for live-service games. It ingests player feedback from Reddit, classifies it with NLP, ranks problem areas by severity, and turns repeated complaints into tracked issues that a dev team can act on.

The demo data is built around EA FC, but the architecture is general enough to work for any game with an active subreddit.

## Architecture

Pulse is split into five services:

- Gateway: FastAPI service for JWT auth, rate limiting, routing, and health checks
- Ingestion: FastAPI service for seed-data loading and Reddit ingestion
- Processing: FastAPI service for classification, sentiment, keywords, and severity scoring
- Analytics: Spring Boot service for trends, rankings, and patch impact
- Issues: FastAPI service for issue generation, lifecycle tracking, and alerts

Shared infrastructure:

- PostgreSQL 16 for application data
- Redis 7 for rate limiting
- Docker Compose for local orchestration

The gateway on `http://localhost:8000` is the main entry point. Backend services run on the internal Docker network.

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- Pydantic
- Java 17
- Spring Boot
- PostgreSQL
- Redis
- HuggingFace Transformers
- Docker Compose

## Quick Start

```bash
git clone <repo-url>
cd pulse
cp .env.example .env
docker compose up --build
```

Open the gateway docs:

```text
http://localhost:8000/docs
```

Log in through the gateway:

```text
POST /api/auth/login
```

Default credentials:

```json
{
  "username": "pulse_admin",
  "password": "pulse_admin"
}
```

Authorize Swagger with:

```text
Bearer <token>
```

## Typical Demo Flow

Run these in order through the gateway:

```text
POST /api/ingest/seed
POST /api/process/batch
POST /api/issues/auto-generate
GET  /api/trends/overview
GET  /api/rankings
GET  /api/issues?page=1&page_size=5
```

## Testing

For a full-stack smoke test on Windows PowerShell:

```powershell
.\scripts\smoke-test.ps1
```

For the same smoke test plus negative-path checks:

```powershell
.\scripts\smoke-test.ps1 -CheckNegativeCases
```

For the gateway unit tests:

```powershell
python -m pip install -r .\services\gateway\requirements-dev.txt
python -m pytest .\services\gateway\tests
```

More detail:

- [Testing Guide](docs/testing.md)
- [Demo Walkthrough](docs/demo-walkthrough.md)

## Services

| Service | Main responsibility |
|---------|----------------------|
| Gateway | Auth, rate limiting, routing, health aggregation |
| Ingestion | Seed and Reddit ingestion, raw post queries |
| Processing | NLP classification, sentiment, keywords, severity |
| Analytics | Trends, rankings, patch impact |
| Issues | Issue generation, lifecycle tracking, alerts |

## What Each Stage Added

- Stage 1: Ingestion pipeline and raw post storage
- Stage 2: NLP processing and severity scoring
- Stage 3: Analytics and patch impact analysis
- Stage 4: Issue generation, lifecycle management, and alerts
- Stage 5: API gateway with JWT auth and rate limiting
- Stage 6: Error handling, test tooling, smoke tests, and final docs polish

## Environment Variables

`.env.example` includes:

- `DATABASE_URL`
- `REDIS_URL`
- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USER_AGENT`
- `JWT_SECRET_KEY`
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `CORS_ORIGINS`

Reddit credentials are optional if you only want to use the seed dataset.

## Repo Structure

```text
pulse/
|-- data/
|   |-- seed_posts.json
|-- docs/
|   |-- demo-walkthrough.md
|   `-- testing.md
|-- scripts/
|   `-- smoke-test.ps1
|-- services/
|   |-- analytics/
|   |-- gateway/
|   |-- ingestion/
|   |-- issues/
|   `-- processing/
|-- docker-compose.yml
`-- README.md
```

## Notes

- The seed dataset is intentionally EA FC-focused.
- Gateway auth is required for normal API use.
- The smoke test script is the fastest way to prove the stack works end to end.
