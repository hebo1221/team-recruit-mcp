# PLAN.md — Work Plan
- Context: Remove legacy HTTP test scripts, keep actionable checks.
- Section 1: Remove root HTTP helpers — Delete `test_simple.sh` and `test_mcp.py`; confirm no other root scripts remain. ✅ Completed.
- Section 2: Drop obsolete Python test scripts — Remove obsolete scripts while ensuring `test_mcp_full.py` remains. ✅ Completed.
- Section 3: Validation & follow-up — Run `node --check src/index.js`, capture status, and update `TODO.md` with next steps. ✅ Completed.
- Section 4: Public release polish — Sanitize tokens/URLs in docs, remove `slack_api_info.md`, align README structure. ✅ Completed.
- Risks/Notes: Avoid deleting maintained integration harnesses; double-check git status after removals.
- Exit Criteria: Target files gone, validation command succeeds, TODO updated.
