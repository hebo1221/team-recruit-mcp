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

### 2. Claude Desktop 설정

**설정 파일 위치**:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

**설정 추가** (경로를 실제 프로젝트 경로로 변경):

```json
{
  "mcpServers": {
    "maicon2025-team-recruit": {
      "command": "/절대경로/mcp-team-recruit/venv/bin/python3",
      "args": [
        "/절대경로/mcp-team-recruit/mcp_stdio.py"
      ]
    }
  }
}
```

**Windows 예시**:
```json
{
  "mcpServers": {
    "maicon2025-team-recruit": {
      "command": "C:\\Users\\YourName\\mcp-team-recruit\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YourName\\mcp-team-recruit\\mcp_stdio.py"
      ]
    }
  }
}
```

### 3. Claude Desktop 재시작

설정을 적용하려면 Claude Desktop을 완전히 종료 후 재시작하세요.

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

1. **경로 확인**: `claude_desktop_config.json`의 경로가 정확한지 확인
2. **JSON 형식 확인**: 쉼표, 중괄호 등이 올바른지 확인
3. **Claude Desktop 재시작**: 완전히 종료 후 재시작

### 터미널에서 직접 테스트

```bash
cd mcp-team-recruit
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | venv/bin/python3 mcp_stdio.py
```

정상 작동하면 JSON 응답이 출력됩니다.

## 📬 문의

팀장 인사말: Claude Desktop에서 `team.greeting()` 실행

## ⏰ 운영 기간

MAICON 팀 빌딩 기간 종료 시 서버도 함께 종료됩니다.

---

**개발 방식**: 100% vibe coding with Claude Code 🤖
