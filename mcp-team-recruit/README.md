# 🎯 MAICON 2025 팀 빌딩 MCP 서버

Claude Desktop에서 바로 팀 지원서를 제출할 수 있는 MCP 서버입니다.

## 🚀 빠른 시작

### 1. 프로젝트 클론 및 설치

```bash
git clone https://github.com/yourusername/mcp-team-recruit.git
cd mcp-team-recruit
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Claude Desktop HTTP 커넥터 등록

1. Claude Desktop을 실행하고 **Settings → Connectors** 메뉴로 이동합니다.
2. **Add custom connector**를 선택하고 아래 값을 입력합니다.

```json
{
  "name": "MAICON 2025 Team Recruit",
  "url": "https://maicon2025-team-recruit-278861544731.asia-northeast3.run.app/mcp",
  "headers": {
    "Accept": "application/json, text/event-stream"
  }
}
```

> 인증 토큰을 사용 중이라면 `headers`에 `Authorization` 헤더를 함께 추가하세요.

3. 저장한 뒤 Claude Desktop을 재시작하면 커넥터가 목록에 나타납니다.

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

## 📝 지원서 제출 예시

```
team.apply() 도구로 지원서를 제출해줘.

이름: 홍길동
연락처: hong@example.com
구분: 장병
메시지: Python과 ML에 관심이 많습니다.
AI 구독: Claude Pro
```

## 💡 참고사항

- **지원 대상**: 장병, 사관생도만 지원 가능
- **일반인**: 안타깝게도 대회 규정상 일반인 지원은 불가능합니다
- **알림**: 지원서 제출 시 팀장의 Slack으로 즉시 알림 전송

## 🛠️ 문제 해결

### MCP 서버가 연결되지 않을 때

1. **HTTP 헤더 확인**: `Accept` 헤더에 `application/json`과 `text/event-stream`이 모두 포함되어야 합니다.
2. **Authorization**: 토큰을 요구하는 환경이라면 `Authorization: Bearer <TOKEN>`을 함께 전달하세요.
3. **재시작**: 커넥터 추가 후 Claude Desktop을 완전히 종료했다가 다시 실행해 주세요.

### 터미널에서 직접 테스트

```bash
curl -i \
  -X POST "https://maicon2025-team-recruit-278861544731.asia-northeast3.run.app/mcp" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"clientInfo":{"name":"curl","version":"1.0"},"protocolVersion":"2024-11-05"}}'
```

`HTTP/2 200`과 함께 `event: message` 형태의 SSE 응답이 내려오면 정상입니다.

## 📬 문의

팀장 인사말: Claude Desktop에서 `team.greeting()` 실행

## ⏰ 운영 기간

MAICON 팀 빌딩 기간 종료 시 서버도 함께 종료됩니다.

---

**개발 방식**: 100% vibe coding with Claude Code 🤖
