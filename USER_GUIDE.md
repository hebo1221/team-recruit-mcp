# 👤 이용자 가이드: MCP로 팀 지원하기

## 🎯 개요

이 가이드는 **실제 지원자가 MCP(Model Context Protocol)를 통해 팀에 지원하는 방법**을 설명합니다.

---

## 📋 사전 준비

### 필요한 것
1. **MCP 서버 URL**: `http://localhost:8080/` (또는 배포된 URL)
2. **Bearer 토큰**: `81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474`
3. **MCP 클라이언트**:
   - Claude Desktop (Pro/Team/Enterprise)
   - MCP Inspector (무료)
   - 기타 MCP 호환 클라이언트

---

## 🚀 방법 1: Claude Desktop으로 지원 (권장)

### Step 1: Claude Desktop 설정

1. **Settings 열기**
   - macOS: `⌘ ,`
   - Windows: `Ctrl ,`

2. **Developer → Edit Config 클릭**

3. **다음 설정 추가**:

**중요**: Claude Desktop은 로컬 MCP 서버에 직접 연결할 수 없습니다.
대신 **MCP Inspector** 또는 **배포된 원격 서버**를 사용하세요.

로컬 테스트용 설정:
```json
{
  "mcpServers": {
    "team-recruit": {
      "command": "/Users/junghunkim/💻_Development/02_🏢_스타트업/hiring/mcp-team-recruit/venv/bin/python",
      "args": ["/Users/junghunkim/💻_Development/02_🏢_스타트업/hiring/mcp-team-recruit/mcp_stdio.py"]
    }
  }
}
```

**주의**: 환경 변수는 `mcp_stdio.py`에 하드코딩되어 있습니다

**권장**: GCP Cloud Run 배포 후 원격 URL 사용

4. **Save → Restart Claude Desktop**

---

### Step 2: 연결 확인

새 대화를 시작하고:

```
team.ping()
```

**예상 응답**: `pong ✅`

---

### Step 3: 팀 정보 확인

#### FAQ 보기
```
team.faq()
```

#### 모집 역할 확인
```
리소스 roles://openings를 읽어줘
```

#### 대회 일정 확인
```
리소스 event://timeline을 읽어줘
```

---

### Step 4: 지원서 작성 도우미

```
intro_template 프롬프트를 사용해서 Vision Engineer 지원 양식을 보여줘
```

---

### Step 5: 지원서 제출

```
team.apply 도구를 사용해서 다음 정보로 지원서를 제출해줘:

이름: 홍길동
이메일: hong@example.com
역할: Vision Engineer
GitHub: https://github.com/hong
스킬: YOLO, OpenCV, PyTorch, CUDA
주당 가능 시간: 20시간
메시지: 컴퓨터 비전 분야 3년 경력. 실시간 객체 인식 시스템 개발 경험 있습니다.
```

Claude가 자동으로 JSON 형식으로 변환해서 제출합니다.

---

### Step 6: 제출 확인

성공 시 다음과 같은 응답:

```json
{
  "ok": true,
  "message": "지원해주셔서 감사합니다, 홍길동님! 빠른 시일 내에 연락드리겠습니다.",
  "notifications": {
    "saved": true,
    "slack_notified": true
  }
}
```

---

## 🔍 방법 2: MCP Inspector로 지원 (개발자용)

### Step 1: MCP Inspector 실행

```bash
npx @modelcontextprotocol/inspector
```

### Step 2: 연결 설정

- **Transport**: Streamable HTTP
- **URL**: `http://localhost:8080/`
- **Header 추가**:
  - Name: `Authorization`
  - Value: `Bearer 81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474`

### Step 3: Connect 클릭

### Step 4: 지원서 제출

1. **Tools 탭** → **apply** 선택
2. **Arguments** 입력:

```json
{
  "payload": {
    "name": "홍길동",
    "email": "hong@example.com",
    "role": "Vision Engineer",
    "github": "https://github.com/hong",
    "skills": ["YOLO", "OpenCV", "PyTorch", "CUDA"],
    "time_per_week": 20,
    "notes": "컴퓨터 비전 분야 3년 경력. 실시간 객체 인식 시스템 개발 경험 있습니다."
  }
}
```

3. **Execute** 클릭

---

## 📝 지원서 작성 팁

### 필수 항목
- ✅ **이름**: 실명 (2-50자)
- ✅ **이메일**: 유효한 이메일 주소
- ✅ **역할**: Vision/LLM/MLOps/Backend/Frontend/PM
- ✅ **주당 시간**: 1-80 사이 숫자

### 선택 항목 (권장)
- 📌 **GitHub**: 프로필 URL
- 📌 **포트폴리오**: 개인 웹사이트, 블로그
- 📌 **스킬**: 관련 기술 스택 (배열)
- 📌 **메시지**: 경험, 목표 등 (최대 1000자)

### 검증 오류 예시

❌ **잘못된 이메일**:
```json
{
  "email": "invalid-email"  // @ 없음
}
```

❌ **시간 범위 초과**:
```json
{
  "time_per_week": 100  // 1-80 범위 초과
}
```

---

## 🎉 제출 후 확인

### 1. 로컬 파일 확인 (개발자만)
```bash
cat data/applicants.jsonl | grep "hong@example.com"
```

### 2. Slack 알림 확인
- 팀 Slack 채널에 알림 도착
- 이름, 역할, 스킬 등 정보 표시

---

## ❓ FAQ

### Q1. 지원서 수정이 가능한가요?
A. 현재는 수정 기능이 없습니다. 재제출하거나 이메일로 연락 주세요.

### Q2. 토큰은 어디서 받나요?
A. 팀 빌딩 게시글의 연락처로 요청하세요.

### Q3. MCP가 없으면 지원할 수 없나요?
A. 일반 이메일이나 구글폼으로도 지원 가능합니다.

### Q4. 어떤 정보가 저장되나요?
A. 제출한 모든 정보 + 타임스탬프가 저장됩니다.

---

## 📞 문의

- **일반 문의**: recruit@example.com
- **기술 지원**: MCP 연결 문제 시 이메일 문의

---

## 🔒 개인정보 처리

- 제출된 정보는 팀 구성 목적으로만 사용됩니다.
- 대회 종료 후 30일 이내 파기됩니다.
- 슬랙 알림은 팀 내부 채널에만 전송됩니다.
