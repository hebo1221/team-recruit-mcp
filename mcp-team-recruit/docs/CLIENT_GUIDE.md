# 지원자용 MCP 연결 가이드

이 문서는 MCP(Model Context Protocol)를 통해 팀에 지원하는 방법을 안내합니다.

## 📋 사전 준비

### 1. MCP 토큰 받기
- 팀 빌딩 게시글의 연락처로 토큰을 요청하세요
- 이메일 또는 구글폼을 통해 발급받을 수 있습니다

### 2. MCP 클라이언트 선택

다음 중 하나를 사용할 수 있습니다:

#### Option A: Claude Desktop (권장)
- **요구사항**: Claude Pro, Team, 또는 Enterprise 계정
- **장점**: 가장 사용하기 쉬움, GUI 제공

#### Option B: MCP Inspector
- **요구사항**: Node.js 18+
- **장점**: 무료, 빠른 테스트 가능

#### Option C: 기타 MCP 호환 클라이언트
- Cursor
- Amazon Q CLI
- 기타 MCP 구현체

---

## 🚀 연결 방법

### Option A: Claude Desktop으로 연결

#### 1. Claude Desktop 설정 열기
- macOS: `⌘ ,` 또는 메뉴 → Settings
- Windows: `Ctrl ,` 또는 메뉴 → Settings

#### 2. Connectors 탭으로 이동
- 왼쪽 사이드바에서 "Connectors" 선택

#### 3. Custom Connector 추가
- "Add custom connector" 버튼 클릭
- 다음 정보 입력:

```json
{
  "name": "팀 리크루팅",
  "url": "https://mcp.example.com/",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN_HERE"
  }
}
```

**주의**: `YOUR_TOKEN_HERE`를 실제 받은 토큰으로 교체하세요!

#### 4. 연결 테스트
새 대화를 시작하고 다음 명령어를 입력:

```
team.ping()
```

응답으로 `pong ✅`가 오면 성공입니다!

---

### Option B: MCP Inspector로 연결

#### 1. Inspector 실행
터미널에서:

```bash
npx @modelcontextprotocol/inspector
```

#### 2. 서버 정보 입력
- **URL**: `https://mcp.example.com/`
- **Headers**:
  - Name: `Authorization`
  - Value: `Bearer YOUR_TOKEN_HERE`

#### 3. Connect 클릭

#### 4. 툴 테스트
- 왼쪽 "Tools" 탭에서 `team.ping` 선택
- "Execute" 클릭

---

## 📝 지원서 작성 및 제출

### 1. FAQ 확인 (선택)
```
team.faq()
```

### 2. 모집 역할 확인
리소스 탭에서 `roles://openings` 조회

### 3. 자기소개 양식 받기
```
intro_template(role="Vision Engineer")
```
※ `role`은 희망 역할로 변경

### 4. 지원서 제출
```python
team.apply({
  "name": "김정훈",
  "contact": "kjh@example.com",
  "category": "장병",
  "message": "도로교통 영상 인식 프로젝트 3건 경험. DeepStream 최적화에 관심 많습니다.",
  "ai_subscriptions": "Claude Pro"
})
```

#### 필수 필드
- `name`: 이름 (문자열, 2-50자)
- `contact`: 연락처 (이메일, 전화번호, 오픈채팅 등 5-200자)
- `category`: 구분 ("장병" / "사관생도" / "일반인")

#### 선택 필드
- `message`: 자기소개/경험 (문자열, 최대 2000자)
- `ai_subscriptions`: 현재 구독 중인 AI 서비스 (문자열, 최대 500자)

### 5. 제출 확인
성공 시 다음과 같은 응답을 받습니다:

```json
{
  "ok": true,
  "message": "지원해주셔서 감사합니다, 김정훈님! 빠른 시일 내에 연락드리겠습니다.",
  "normalized": { ... },
  "notifications": {
    "saved": true,
    "slack_notified": true
  }
}
```

---

## 🛠️ 트러블슈팅

### 연결 오류
**증상**: `Connection failed` 또는 `401 Unauthorized`

**해결**:
1. URL이 정확한지 확인 (https://... 포함)
2. 토큰이 `Bearer ` 접두사와 함께 올바르게 입력되었는지 확인
3. 토큰 만료 여부 확인 (재발급 요청)

### 지원서 검증 오류
**증상**: `"ok": false, "error": [...]`

**해결**:
1. 에러 메시지의 `error` 배열 확인
2. 필수 필드(`name`, `contact`, `category`)가 모두 포함되었는지 확인
3. 연락처 길이가 5자 이상인지 확인
4. 구분이 허용된 값인지 확인 (장병/사관생도/일반인)

### MCP Inspector가 실행되지 않음
**증상**: `npx` 명령 실패

**해결**:
```bash
# Node.js 버전 확인 (18 이상 필요)
node --version

# 필요시 Node.js 설치/업데이트
# https://nodejs.org/
```

---

## 📚 추가 리소스

### 사용 가능한 도구 (Tools)
- `team.ping()` - 연결 테스트
- `team.faq()` - 대회 및 팀 FAQ
- `team.apply(payload)` - 지원서 제출

### 사용 가능한 리소스 (Resources)
- `roles://openings` - 모집 역할 및 요구사항
- `event://timeline` - 대회 일정

### 사용 가능한 프롬프트 (Prompts)
- `intro_template(role)` - 역할별 자기소개 양식

---

## 💬 문의

MCP 연결에 어려움이 있거나 질문이 있으시면:
- **이메일**: recruit@example.com
- **일반 지원**: [구글폼 링크]

MCP를 사용하지 않고도 일반 경로로 지원 가능합니다!
