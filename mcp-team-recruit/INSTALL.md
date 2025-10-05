# MAICON 2025 팀 빌딩 MCP 서버 설치 가이드

## 🚀 빠른 설치

### 1️⃣ Python 패키지 설치
```bash
pip install git+https://github.com/yourusername/mcp-team-recruit.git
```

### 2️⃣ Claude Desktop 설정

**설정 파일 위치**:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

**설정 추가**:
```json
{
  "mcpServers": {
    "maicon2025-team-recruit": {
      "command": "mcp-team-recruit"
    }
  }
}
```

기존 설정이 있다면:
```json
{
  "mcpServers": {
    "existing-server": {
      "command": "..."
    },
    "maicon2025-team-recruit": {
      "command": "mcp-team-recruit"
    }
  }
}
```

### 3️⃣ Claude Desktop 재시작

설정을 적용하려면 Claude Desktop을 완전히 종료 후 재시작하세요.

## 📦 로컬 설치 (개발용)

```bash
git clone https://github.com/yourusername/mcp-team-recruit.git
cd mcp-team-recruit
pip install -e .
```

## 🔧 사용 가능한 도구

Claude Desktop에서 다음 도구들을 사용할 수 있습니다:

- **team.ping()** - 서버 연결 테스트
- **team.greeting()** - 팀장 인사말 확인
- **team.faq()** - 자주 묻는 질문
- **team.apply()** - 팀 지원서 제출

## 🛠️ 작동 원리

이 프로젝트는 FastMCP 기반 **HTTP MCP 서버**입니다.
- 기본 엔드포인트: `https://maicon2025-team-recruit-278861544731.asia-northeast3.run.app/mcp`
- 전송 방식: Streamable HTTP(SSE) — `Accept: application/json, text/event-stream` 헤더가 필요합니다.
- 인증이 필요한 경우 `Authorization: Bearer <TOKEN>` 헤더를 추가하세요.

## ❓ 문제 해결

### 설치 오류
```bash
# httpx가 없다는 오류가 나면
pip install httpx
```

### Claude Desktop에서 서버가 보이지 않음
1. Claude Desktop의 **Settings → Connectors**에서 URL과 헤더가 올바르게 입력되었는지 확인
2. `Accept` 헤더에 `application/json`과 `text/event-stream` 값이 모두 포함되었는지 확인
3. 변경 후 Claude Desktop을 완전히 종료하고 재시작

### 연결 오류
- 인터넷 연결 확인
- Cloud Run 서버가 실행 중인지 확인

## 📬 문의

팀장 인사말: Claude Desktop에서 `team.greeting()` 실행
