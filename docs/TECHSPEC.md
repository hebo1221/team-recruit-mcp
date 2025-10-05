TECHSPEC — MCP Team Recruit (HTTP)
=================================

Scope
- Single server: Python FastMCP over streamable HTTP (SSE) only.
- Endpoint: `POST /mcp` (JSON-RPC over HTTP with SSE responses).
- Health: `GET /healthz` → 200 `ok`.

Transport
- Request: `Content-Type: application/json`.
- Accept: Must include `application/json, text/event-stream` (auto-normalized by middleware if missing).
- Responses: SSE stream with `event: message` frames carrying JSON-RPC payloads.

Auth
- Header: `Authorization: Bearer <MCP_API_KEY>` when `MCP_API_KEY` env is set (recommended for prod).
- Unauthorized: 401 with `WWW-Authenticate: Bearer`.

Tools
- `ping()` → text "pong ✅"
- `greeting()` → team leader intro (text)
- `faq()` → team FAQ (text)
- `apply(payload: Applicant)` → JSON result, Slack notify optional

Applicant Schema
- name: 2–50
- contact: 5–200 (PII masked in logs)
- category: string (e.g., 장병/사관생도/일반인)
- message/motivation/experience: ≤2000
- organization: ≤200
- portfolio_url/ai_subscriptions: ≤500

Storage
- Local JSONL append at `data/applicants.jsonl`.
- Cloud Run concurrency set to 1 by default; move to SQLite/Firestore/GCS before raising concurrency.

Security Notes
- Do not commit secrets; use env or secret manager.
- Rate limit and request size limits recommended for public endpoints.

Testing
- In-process ASGI integration test: `mcp-team-recruit/test_mcp_full.py`.
