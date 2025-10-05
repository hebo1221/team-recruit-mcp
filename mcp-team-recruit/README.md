# 🎯 MAICON 2025 팀 빌딩 MCP 서버

MCP(Model Context Protocol)를 통해 팀 지원서를 제출하고 팀 정보를 조회할 수 있는 HTTP 기반 서버입니다.

## 🚀 빠른 시작

### 1. 프로젝트 클론 및 설치

```bash
git clone https://github.com/yourusername/mcp-team-recruit.git
cd mcp-team-recruit
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. MCP 클라이언트 설정

- **Claude Desktop**: **Settings → Connectors → Add custom connector**에서 다음 값을 입력하세요.

  ```json
  {
    "name": "MAICON 2025 Team Recruit",
    "url": "https://<YOUR_DEPLOYED_URL>/mcp"
  }
  ```

- **Cursor 등 기타 MCP 클라이언트**: 설정 파일에 동일한 URL을 등록하면 됩니다.
  ```json
    "maicon2025-team-recruit": {
      "url": "https://<YOUR_DEPLOYED_URL>/mcp"
    }
  ```
> 인증 토큰이 필요한 환경이라면 `Authorization: Bearer <TOKEN>` 헤더를 추가하세요.

## 🔧 사용 방법

Claude Desktop 채팅에서 다음과 같이 사용하세요:

```
team.ping() 도구를 실행해줘
```

### 사용 가능한 도구

- **team.ping()** - 서버 연결 테스트
- **team.greeting()** - 팀장 인사말 확인
- **team.faq()** - 자주 묻는 질문
- **team.apply()** - 팀 지원서 제출

Tip: 실제 지원에서는 모든 상세 내용을 `message` 필드 하나에 한 번에 서술하고, `motivation`, `experience`, `organization`, `portfolio_url`, `ai_subscriptions` 등 선택 항목도 필요에 따라 채워 주세요. LLM을 사용할 경우 `team.apply(payload={...})` 형태로 정확한 키를 사용하고, 제출 전 필수 필드와 길이를 다시 점검하세요.

## 📝 지원서 제출 예시

```
team.apply() 도구로 지원서를 제출해줘.

이름: 홍길동
연락처: hong@example.com
구분: 장병
메시지: Python과 ML에 관심이 많습니다.
AI 구독: Claude Pro
```

## 🛠️ 문제 해결

### MCP 서버가 연결되지 않을 때

1. **헤더 확인**: 토큰이 필요한 환경이라면 `Authorization: Bearer <TOKEN>`을 전달하세요.
2. **재시작**: 커넥터 추가 후 클라이언트를 완전히 종료했다가 다시 실행해 주세요.

### 터미널에서 직접 테스트

```bash
curl -i \
  -X POST "https://<YOUR_DEPLOYED_URL>/mcp" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -H 'Authorization: Bearer <YOUR_TOKEN>' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"curl","version":"1.0"},"protocolVersion":"2024-11-05"}}'
```

`HTTP/2 200`과 함께 `event: message` 형태의 SSE 응답이 내려오면 정상입니다.

### 헬스체크
```
curl -i "https://<YOUR_DEPLOYED_URL>/healthz"
```
`200 OK`와 본문 `ok`이면 정상입니다.

## 📬 문의

팀장 인사말: Claude Desktop에서 `team.greeting()` 실행

## ⏰ 운영 기간

MAICON 팀 빌딩 기간 종료 시 서버도 함께 종료됩니다.
