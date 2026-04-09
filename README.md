# Pulse

Community intelligence platform for live-service games. Pulls player feedback from Reddit, classifies it with NLP, ranks issues by severity, and tracks how patches affect community sentiment.

Built around EA FC as the demo dataset, but the architecture works for any game with an active subreddit.

## What it does

Players complain on Reddit about their favorite games. Pulse turns that noise into signal:

1. **Ingests** posts from Reddit (or seed data) and stores them
2. **Classifies** each post by category (gameplay bug, UI bug, balance, server issues, etc.) and runs sentiment analysis
3. **Ranks** issues by a composite severity score and compares community health before vs after patches
4. **Auto-generates issues** by clustering related complaints — like a bug tracker that populates itself
5. **Fires alerts** when complaint volume spikes past configurable thresholds

Everything runs through a single API gateway with JWT auth and rate limiting.

## Architecture

Five services, one database, one cache. Everything containerized.

```
Gateway :8000 (auth, rate limiting, routing)
  ├── Ingestion  :8001  (Python/FastAPI)
  ├── Processing :8002  (Python/FastAPI)
  ├── Analytics  :8003  (Java/Spring Boot)
  └── Issues     :8004  (Python/FastAPI)

PostgreSQL — shared database
Redis — rate limiting + caching
```

## Tech stack

- **Python/FastAPI** — ingestion, processing, issues, gateway
- **Java/Spring Boot** — analytics service
- **PostgreSQL 16** — primary database
- **Redis 7** — rate limiting
- **HuggingFace Transformers** — sentiment analysis (cardiffnlp/twitter-roberta-base)
- **Docker Compose** — runs everything with one command

## Quick start

```bash
git clone <repo-url>
cd pulse
cp .env.example .env
docker-compose up --build
```


## Running the pipeline

Once everything is up, run these in order:

**1. Load seed data** — `http://localhost:8001/docs`
```
POST /api/ingest/seed  →  {"clear_existing": false}
```

**2. Process posts** — `http://localhost:8002/docs`
```
POST /api/process/batch  →  {"batch_size": 50}
```

**3. Check analytics** — `http://localhost:8003/docs`
```
GET /api/trends/overview
GET /api/rankings
```

**4. Generate issues** — `http://localhost:8004/docs`
```
POST /api/issues/auto-generate  →  {}
```

**5. Use the gateway** — `http://localhost:8000/docs`

Login first:
```
POST /auth/login  →  {"username": "admin", "password": "pulse-admin"}
```

Copy the token, click "Authorize" in Swagger, paste `Bearer <token>`. Now all `/api/*` routes go through the gateway with auth and rate limiting.

## Services

| Service | Port | What it does |
|---------|------|-------------|
| Gateway | 8000 | Auth, rate limiting, routes to backend services |
| Ingestion | 8001 | Pulls posts from Reddit or loads seed data |
| Processing | 8002 | NLP classification, sentiment, severity scoring |
| Analytics | 8003 | Trend aggregation, patch impact, issue rankings |
| Issues | 8004 | Auto-generated issue tracker with alerts |

## Reddit integration (optional)

If you want live Reddit data:

1. Go to https://www.reddit.com/prefs/apps
2. Create a "script" type application
3. Add your credentials to `.env`:
```
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
```
4. Hit `POST /api/ingest/reddit` on port 8001

## Project structure

```
pulse/
├── docker-compose.yml
├── data/seed_posts.json          # 30 hand-picked EA FC community posts
├── services/
│   ├── gateway/                  # Python — auth, rate limiting, routing
│   ├── ingestion/                # Python — Reddit API, seed loading
│   ├── processing/               # Python — NLP pipeline
│   ├── analytics/                # Java  — trends, rankings, patch impact
│   └── issues/                   # Python — issue tracking, alerts
└── .env.example
```