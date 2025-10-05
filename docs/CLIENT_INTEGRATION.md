Client Integration Notes
========================

DEPRECATED: 이 문서는 과거 Node stdio(JSON-RPC over stdio) 서버 연동 예시를 다룹니다.
현재 저장소는 Python 기반 HTTP MCP 서버(`mcp-team-recruit/`)만을 제공합니다. 아래 내용은
역사적 참고용으로 유지되며, 실제 사용은 `mcp-team-recruit/README.md`와 `INSTALL.md`를 참고하세요.

Goal
- Participants build a chat/community app with Google Login that connects to this server over MCP-style stdio JSON-RPC.

High-level Flow
1) Implement Google Login in your app (web/native) and obtain a Google ID token (OIDC ID token).
2) Spawn this server as a process and speak JSON-RPC with Content-Length framing over stdio.
3) Call `initialize` → `tools/list` to discover tools.
4) Call `tools/call` for `auth.exchangeGoogleIdToken` with the ID token.
5) Use `community.*` tools under the session to build chat/community UX.

Obtaining a Google ID Token (Web Example)
- Use Google Identity Services for Web (One Tap or button).
- Configure your OAuth client in Google Cloud Console and set authorized origins.
- After login, extract the ID token (JWT string) from the credential response.

Spawning the Server (Node/Electron Example)
```js
import { spawn } from 'node:child_process';

function startServer() {
  const child = spawn('node', ['src/index.js'], {
    stdio: ['pipe', 'pipe', 'pipe']
  });
  return child;
}

function send(child, obj) {
  const json = JSON.stringify(obj);
  const body = Buffer.from(json, 'utf8');
  const header = Buffer.from(`Content-Length: ${body.length}\r\n\r\n`);
  child.stdin.write(Buffer.concat([header, body]));
}

function onData(buffer, handler) {
  // Implement the same Content-Length parser as the server or reuse a library
}
```

Calling Tools
```js
// initialize
send(child, { jsonrpc: '2.0', id: 1, method: 'initialize', params: {} });

// list tools
send(child, { jsonrpc: '2.0', id: 2, method: 'tools/list' });

// exchange Google ID token
send(child, {
  jsonrpc: '2.0', id: 3, method: 'tools/call',
  params: { name: 'auth.exchangeGoogleIdToken', arguments: { idToken } }
});

// create and use rooms
send(child, {
  jsonrpc: '2.0', id: 4, method: 'tools/call',
  params: { name: 'community.createRoom', arguments: { name: 'General' } }
});
```

UI/UX Tips
- Room list on left, messages in center, composer at bottom.
- After posting, call `community.listMessages` periodically or with an incremental `afterTs` for polling.
- Show profile info from the auth result (email/name) for display names.

Security Checklist (Production)
- Verify ID token signature via Google JWKS; check `aud`, `iss`, `exp`.
- Store sessions securely per connection; avoid passing tokens in tool args repeatedly.
- Apply server-side rate limiting; validate all input against schema limits.
- Consider moderation tools, message size limits, and abuse prevention.
