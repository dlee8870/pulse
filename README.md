# Pulse

**Live-Service Game Community Intelligence Platform**

Pulse transforms scattered community feedback into structured, prioritized, data-backed intelligence for game developers. It ingests posts from community sources, processes them through an NLP pipeline to classify and cluster feedback, tracks issue trends over time, and correlates complaint patterns with game patches.

## Architecture

```
┌──────────────────────┐
│     API Gateway       │
│   (Python/FastAPI)    │
└──┬───┬───┬───┬───────┘
   │   │   │   │
   ▼   ▼   ▼   ▼
┌──────┐┌──────┐┌──────┐┌──────┐
│Ingest││Proc. ││Anal. ││Issue │
│(Py)  ││(Py)  ││(Java)││(Py)  │
└──┬───┘└──┬───┘└──┬───┘└──┬───┘
   └───────┴───┬───┴───────┘
               │
        ┌──────┴──────┐
        │ PostgreSQL  │
        │ Redis       │
        └─────────────┘
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Python Services | FastAPI, SQLAlchemy, Pydantic |
| Java Service | Spring Boot, Spring Data JPA |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| NLP | HuggingFace Transformers, spaCy |
| Containers | Docker, Docker Compose |
| API Docs | Swagger / OpenAPI (auto-generated) |

## Quick Start

### Prerequisites

- Docker Desktop
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd pulse
   ```

2. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

3. Start all services:
   ```bash
   docker-compose up --build
   ```

4. Open the Ingestion Service API docs:
   ```
   http://localhost:8001/docs
   ```

5. Load seed data (in the Swagger UI, execute `POST /api/ingest/seed`):
   ```json
   {
     "clear_existing": false
   }
   ```

6. Query posts:
   ```
   GET http://localhost:8001/api/posts?page=1&page_size=10
   ```

### Reddit Integration (Optional)

To pull live data from Reddit:

1. Go to https://www.reddit.com/prefs/apps
2. Create a new application (select "script" type)
3. Copy the client ID and secret into your `.env` file
4. Use the `POST /api/ingest/reddit` endpoint

## Services

| Service | Port | Description |
|---------|------|-------------|
| Ingestion | 8001 | Data ingestion from Reddit and seed files |
| Processing | 8002 | NLP classification, sentiment analysis, entity extraction |
| Analytics | 8003 | Trend analysis, patch correlation, issue ranking |
| Issues | 8004 | Auto-generated issue tracking and alerts |
| Gateway | 8000 | Unified API entry point with auth and routing |

## Project Status

- [x] Stage 1: Foundation + Ingestion Service
- [ ] Stage 2: NLP Processing Pipeline
- [ ] Stage 3: Analytics Engine (Java/Spring Boot)
- [ ] Stage 4: Issue Management
- [ ] Stage 5: API Gateway + Integration
- [ ] Stage 6: Polish + Portfolio Ready
