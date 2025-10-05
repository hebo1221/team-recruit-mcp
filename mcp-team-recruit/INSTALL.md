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

이 패키지는 HTTP MCP 서버(Cloud Run 배포)와 통신하는 간단한 wrapper입니다:
- Cloud Run 서버: `https://maicon2025-team-recruit-278861544731.asia-northeast3.run.app/mcp`
- Wrapper: HTTP 요청을 stdio로 변환하여 Claude Desktop과 통신

## ❓ 문제 해결

### 설치 오류
```bash
# httpx가 없다는 오류가 나면
pip install httpx
```

### Claude Desktop에서 서버가 보이지 않음
1. 설정 파일 경로가 맞는지 확인
2. JSON 형식이 올바른지 확인 (쉼표, 중괄호 등)
3. Claude Desktop을 완전히 종료 후 재시작

### 연결 오류
- 인터넷 연결 확인
- Cloud Run 서버가 실행 중인지 확인

## 📬 문의

팀장 인사말: Claude Desktop에서 `team.greeting()` 실행
