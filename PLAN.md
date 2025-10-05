# PLAN.md — Work Plan
- Context: Consolidate on Python HTTP MCP server; harden security/ops.
- Section 1: Deprecate Node stdio path — Remove `src/index.js`, `package.json`, mark docs deprecated. ✅ Completed.
- Section 2: Security hardening — Add Bearer auth, PII masking, rotate leaked secrets. ✅ Completed.
- Section 3: Ops endpoints — Add `/healthz`, set Cloud Run concurrency 1. ✅ Completed.
- Section 4: Tests & docs — Update integration test for auth; align client guide/readme; add final test report. ✅ Completed.
- Risks/Notes: File-based storage is single-writer; increase concurrency only after moving to durable storage.
- Exit Criteria: HTTP-only server with auth/healthz; docs/tests reflect current behavior; no active secrets in repo.
