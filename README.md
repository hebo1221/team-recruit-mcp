# team-recruit-mcp

# MAICON 2025 팀 빌딩 MCP 서버 (Overview)

이 저장소는 MAICON 팀 빌딩을 위한 MCP 서버와 문서를 포함합니다. 기본 사용 경로는 HTTP 기반 MCP 서버이며, 상세 가이드는 하위 문서를 참고하세요.

- 사용 가이드: mcp-team-recruit/README.md
- 설치/연결: mcp-team-recruit/INSTALL.md

Claude Desktop 커넥터 빠른 설정
- Settings → Connectors → Add custom connector
- name: MAICON 2025 Team Recruit
- url: https://maicon2025-team-recruit-278861544731.asia-northeast3.run.app/mcp
- headers: Accept: application/json, text/event-stream
- 인증이 필요한 경우 Authorization: Bearer <TOKEN>

터미널 초기화 테스트(curl)
- curl -i -X POST "https://maicon2025-team-recruit-278861544731.asia-northeast3.run.app/mcp" \\
  -H 'Content-Type: application/json' \\
  -H 'Accept: application/json, text/event-stream' \\
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"curl","version":"1.0"},"protocolVersion":"2024-11-05"}}'

환경 변수(선택)
- MCP_API_KEY: 서버 접근 토큰 (프록시/네트워크 경계 사용 권장)
- SLACK_WEBHOOK_URL: 지원서 제출 시 Slack 알림 전송용

레포 구조
- mcp-team-recruit/: FastMCP HTTP 서버(파이썬)
- src/index.js: 참고용 stdio MCP 예제(Node) — 유지관리 대상 아님

아래 섹션은 참고용 Node stdio 예제 설명입니다.

OpenCommunity MCP Server
========================

Minimal MCP-like stdio JSON-RPC server exposing auth and community tools so participants can build their own clients (with Google Login) and connect to a shared open community.

Quick Start
-
- Requires Node.js 18+
- Run: `npm start`

Transport
- Uses Content-Length framed JSON-RPC over stdio (MCP style).
- Implements: `initialize`, `tools/list`, `tools/call`, `resources/list`, `resources/read`, `shutdown`, `exit`.

Tools
- `help` — quick intro and flow
- `auth.exchangeGoogleIdToken` — exchange a Google ID token for a session (demo: signature NOT verified)
- `community.listRooms` — list public rooms
- `community.createRoom` — create a room (requires auth)
- `community.postMessage` — post a message (requires auth)
- `community.listMessages` — list recent messages

Client Flow (for contest participants)
- Obtain Google ID token in your client app (web/native) via OAuth 2.0 / OIDC.
- Start the server process and speak JSON-RPC over stdio.
- Call `initialize` → `tools/list` to discover tools.
- Call `auth.exchangeGoogleIdToken` with the ID token.
- Use `community.*` tools for chat/community features.

Claude Desktop Example
- Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```
{
  "mcpServers": {
    "open-community": {
      "command": "node",
      "args": ["src/index.js"],
      "disabled": false
    }
  }
}
```

Security Notes
- Demo server only parses JWT; it does not verify Google signatures.
- For production, verify the ID token using Google JWKS and audience checks.
- Consider per-connection sessions and rate limiting.
