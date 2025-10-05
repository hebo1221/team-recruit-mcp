# TECHSPEC — Legacy Test Cleanup (Round 2)

## Context
- Active product is the Node-based stdio MCP server in `src/index.js`.
- The `mcp-team-recruit/` Python project was the previous HTTP MCP implementation and keeps accumulating ad-hoc/manual test scripts.
- Repository root also picked up refreshed HTTP testing helpers even though the HTTP transport is no longer supported.

## Goals
1. Remove the resurrected HTTP smoke helpers in the repository root (`test_simple.sh`, `test_mcp.py`).
2. Delete redundant Python scripts in `mcp-team-recruit/` that exercise obsolete HTTP pathways or require external web services:
   - `test_accept_header_relax.py`
   - `test_apply.py`
   - `test_category_field.py`
   - `test_full_integration.py`
   - `test_http_client.py`
   - `test_military_status.py`
   - `test_slack_integration.py`
   - `test_updated_server.py`
   - `test_user_experience.py`
3. Retain only the comprehensive integration harness `test_mcp_full.py` and the minimal Slack notification probe `test_slack.py` so manual verification remains possible.
4. Document the state in `TODO.md` so future work can focus on stdio-oriented coverage and mockable Slack checks.

## Non-Goals
- Editing any of the remaining Python tests beyond ensuring they stay in place.
- Changing package metadata, installation guides, or the Node server implementation.
- Building replacement automated coverage during this pass.

## Validation Plan
- Confirm each targeted file is removed from the repository.
- Execute `node --check src/index.js` to sanity check the live server entry point.
- Record actions and follow-up tasks in `TODO.md`.
