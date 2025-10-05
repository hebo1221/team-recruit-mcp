# PLAN.md — Work Plan
- Context: Refer to TECHSPEC.md for scope (remove legacy HTTP test scripts, keep actionable checks).
- Section 1: Remove root HTTP helpers — Delete `test_simple.sh` and `test_mcp.py`; confirm no other root scripts remain. ✅ Completed.
- Section 2: Drop obsolete Python test scripts — Remove the nine files listed in TECHSPEC.md while ensuring `test_mcp_full.py` and `test_slack.py` are untouched. ✅ Completed.
- Section 3: Validation & follow-up — Run `node --check src/index.js`, capture status, and update `TODO.md` with next steps. ✅ Completed.
- Risks/Notes: Avoid deleting maintained integration harnesses; double-check git status after removals.
- Exit Criteria: Target files gone, validation command succeeds, TODO updated.
