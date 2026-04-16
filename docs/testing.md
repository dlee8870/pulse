# Testing

Pulse now has two practical testing paths:

1. A PowerShell smoke test for the full stack
2. A small unit test suite for the gateway

## Full-stack smoke test

Start the stack first:

```powershell
docker compose up --build
```

Then run:

```powershell
.\scripts\smoke-test.ps1
```

What it checks:
- gateway health
- login through the gateway
- seed ingestion
- batch processing
- issue auto-generation
- representative read endpoints for posts, processed posts, trends, rankings, and issues

Run the optional negative-path checks too:

```powershell
.\scripts\smoke-test.ps1 -CheckNegativeCases
```

Those checks cover:
- missing bearer token on a protected route
- unknown proxied route
- invalid login payload

Optional parameters:

```powershell
.\scripts\smoke-test.ps1 -BaseUrl "http://localhost:8000" -Username "pulse_admin" -Password "pulse_admin"
```

## Gateway unit tests

The gateway has focused tests for:
- password hashing and verification
- JWT creation and validation
- expired token rejection
- fixed-window rate limiting
- Redis fail-open behavior

Install test dependencies:

```powershell
python -m pip install -r .\services\gateway\requirements-dev.txt
```

Run the tests:

```powershell
python -m pytest .\services\gateway\tests
```
