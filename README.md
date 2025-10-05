# Team Recruit MCP — Public Release

이 저장소는 두 가지 MCP 구성요소를 포함합니다.

- Node stdio MCP 서버: `src/index.js` (주요 구현)
- Python HTTP MCP 서버: `mcp-team-recruit/` (팀 리크루팅용 서버 및 문서)

둘 다 독립적으로 사용할 수 있으며, 저장소 상단의 문서는 일관된 보안/운영 기준으로 정리되었습니다.

Quick Start (Node stdio)
- Requires Node.js 18+
- Run: `npm start`

Repo Structure
- `src/index.js` — OpenCommunity 스타일 stdio JSON-RPC MCP 서버
- `mcp-team-recruit/` — FastMCP 기반 HTTP MCP 서버(배포/가이드 포함)
- `docs/` — 서버 사양 및 클라이언트 통합 안내

Security & Secrets
- Do not commit real tokens or secrets.
- Use env vars like `MCP_API_KEY`, `SLACK_WEBHOOK_URL` via `.env` or your platform’s secret manager.
- Example placeholders are provided in docs; replace with your values at deploy time.

Links
- Python server usage: `mcp-team-recruit/README.md`
- Python install/deploy: `mcp-team-recruit/INSTALL.md`
- Protocol and client notes: `docs/`

Notes
- The Node server uses Content-Length framed JSON-RPC over stdio and implements: `initialize`, `tools/list`, `tools/call`, `resources/list`, `resources/read`, `shutdown`, `exit`.
- The Python server exposes HTTP(S) endpoints compatible with MCP streamable HTTP and includes optional Slack notifications.
