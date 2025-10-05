# 설치 및 설정 가이드 (HTTP MCP 전용)

이 문서는 MAICON 2025 팀 빌딩 MCP 서버를 HTTP 전송 방식으로 사용하기 위한 설정 방법을 다룹니다.

## 1. 의존성 설치

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. 서버 실행 (로컬 개발용)

```bash
export MCP_API_KEY=REDACTED
uvicorn server:app --host 0.0.0.0 --port 8080
```

## 3. Claude Desktop 커넥터 추가

1. **Settings → Connectors** 로 이동합니다.
2. **Add custom connector** 를 선택하고 아래 값을 입력합니다.

```json
{
  "name": "MAICON 2025 Team Recruit",
  "url": "https://maicon2025-team-recruit-278861544731.asia-northeast3.run.app/mcp",
  "headers": {
    "Accept": "application/json, text/event-stream"
  }
}
```

> 토큰이 필요한 환경이라면 `Authorization: Bearer <TOKEN>` 헤더를 함께 추가하세요.

## 4. Cursor / 기타 MCP 클라이언트 설정

`~/.cursor/mcp.json` 예시:

```json
{
  "mcpServers": {
    "maicon2025-team-recruit": {
      "url": "https://maicon2025-team-recruit-278861544731.asia-northeast3.run.app/mcp",
      "headers": {
        "Accept": "application/json, text/event-stream"
      }
    }
  }
}
```

## 5. 연결 테스트

```bash
curl -i \
  -X POST "https://maicon2025-team-recruit-278861544731.asia-northeast3.run.app/mcp" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"curl","version":"1.0"},"protocolVersion":"2024-11-05"}}'
```

응답으로 `HTTP/2 200`과 `event: message`가 확인되면 정상 연결된 것입니다.

## 6. 트러블슈팅

- **406 Not Acceptable**: `Accept` 헤더에 `application/json`과 `text/event-stream`이 모두 포함되어 있는지 확인하세요.
- **401/403 응답**: 토큰이 필요한 환경인지 확인하고 `Authorization` 헤더를 추가하세요.
- **세션 ID 관련 오류**: `initialize` 응답의 `mcp-session-id` 헤더가 노출되었는지 확인하세요. 브라우저 기반 클라이언트는 CORS 노출 헤더가 필요합니다.

## 7. 배포

Cloud Run 배포는 `deploy.sh` 스크립트를 참고하세요.

```bash
export GCP_PROJECT_ID=<PROJECT_ID>
export MCP_API_KEY=<RANDOM_TOKEN>
./deploy.sh
```

배포 후 `Service URL` 로 위의 `curl` 테스트를 실행해 정상 동작을 확인합니다.

