# Demo Walkthrough

This is the shortest clean demo path for Pulse.

## 1. Start the stack

```powershell
docker compose up --build
```

Open:

```text
http://localhost:8000/docs
```

## 2. Explain the architecture

Talk through the flow in one sentence:

> Reddit posts come in through ingestion, get classified and scored by processing, get aggregated by analytics, become tracked issues in the issue service, and all of it is exposed through a JWT-protected API gateway.

## 3. Show authentication

Run:

```text
POST /api/auth/login
```

Use:

```json
{
  "username": "pulse_admin",
  "password": "pulse_admin"
}
```

Then authorize the Swagger UI with:

```text
Bearer <token>
```

## 4. Show the pipeline

Run these in order:

```text
POST /api/ingest/seed
POST /api/process/batch
POST /api/issues/auto-generate
GET  /api/trends/overview
GET  /api/rankings
GET  /api/issues?page=1&page_size=5
```

Points to emphasize:
- ingestion is idempotent because duplicate seed posts are tracked
- processing is idempotent because already-processed posts are skipped
- issue generation clusters unlinked processed posts
- rankings use severity, sentiment, and volume together

## 5. Use the smoke script if needed

If you want a repeatable demo without clicking through Swagger:

```powershell
.\scripts\smoke-test.ps1
```

## 6. Close with the portfolio angle

Key points:
- multi-service architecture
- Python and Java in one project
- shared PostgreSQL data model
- authentication and rate limiting at the gateway
- enough documentation and tooling for someone else to run it
