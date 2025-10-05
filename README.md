# Team Recruit MCP — Public Release

이 저장소는 MAICON 팀 리크루팅을 위한 HTTP 기반 MCP 서버만을 제공합니다.

- Python HTTP MCP 서버: `mcp-team-recruit/` (설치/배포/가이드 포함)

중요: 기존 Node stdio MCP 서버(`src/index.js`)는 더 이상 사용하지 않으며, 저장소에서 제거되었습니다. 필요 시 과거 사양 참고용 문서는 `docs/`에 보관되어 있습니다(Deprecated 표기).

Quick Start (Python HTTP MCP)
- Requires Python 3.10+
- See: `mcp-team-recruit/INSTALL.md`

Repo Structure
- `mcp-team-recruit/` — FastMCP 기반 HTTP MCP 서버(배포/가이드 포함)
- `docs/` — (Deprecated) 과거 stdio 서버 사양/예시, 현재는 참고용 아카이브

Security & Secrets
- Do not commit real tokens or secrets.
- Use env vars like `MCP_API_KEY`, `SLACK_WEBHOOK_URL` via your platform’s secret manager.
- Example placeholders are provided in docs; replace with your values at deploy time.

Links
- Python server usage: `mcp-team-recruit/README.md`
- Python install/deploy: `mcp-team-recruit/INSTALL.md`

Notes
- Python 서버는 MCP streamable HTTP(S) 엔드포인트를 제공하며 선택적으로 Slack 알림을 지원합니다.
