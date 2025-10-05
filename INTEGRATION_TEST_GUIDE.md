# MCP 팀 리크루팅 서버 통합 테스트 가이드

## 🎯 테스트 개요

MCP Inspector를 사용하여 모든 기능을 테스트합니다.

---

## 📋 사전 준비

### 1. 서버 실행 확인
```bash
cd mcp-team-recruit
source venv/bin/activate
python server.py
```

### 2. 헬스체크
```bash
curl http://localhost:8080/healthz
# 응답: ok
```

### 3. MCP Inspector 실행
```bash
npx @modelcontextprotocol/inspector
```

---

## 🔌 MCP Inspector 연결 설정

### 연결 정보 입력

1. **Transport Type**: `Streamable HTTP`
2. **URL**: `http://localhost:8080/`
3. **Headers** (Add Header 클릭):
   - **Name**: `Authorization`
   - **Value**: `Bearer 81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474`

4. **Connect** 버튼 클릭

---

## ✅ 테스트 체크리스트

### 1. Tools 테스트

#### Test 1.1: `ping`
```
도구: ping
인자: (없음)
예상 결과: "pong ✅"
```

**실행 방법**:
- Tools 탭 → `ping` 선택 → Execute

**통과 기준**: ✅ "pong ✅" 응답

---

#### Test 1.2: `faq`
```
도구: faq
인자: (없음)
예상 결과: FAQ 텍스트 (모집분야, 기간, 지원방법)
```

**실행 방법**:
- Tools 탭 → `faq` 선택 → Execute

**통과 기준**: ✅ FAQ 내용 표시 (모집분야 목록 포함)

---

#### Test 1.3: `apply` (정상 케이스)
```json
도구: apply
인자:
{
  "payload": {
    "name": "김정훈",
    "email": "kjh@example.com",
    "role": "Vision Engineer",
    "github": "https://github.com/kjh",
    "skills": ["YOLO", "DeepStream", "PyTorch"],
    "time_per_week": 20,
    "notes": "MCP Inspector 테스트용 지원서입니다."
  }
}
```

**실행 방법**:
- Tools 탭 → `apply` 선택
- Arguments 필드에 위 JSON 입력
- Execute

**통과 기준**:
- ✅ `{"ok": true, "message": "...", "normalized": {...}}`
- ✅ `data/applicants.jsonl` 파일에 저장됨

---

#### Test 1.4: `apply` (유효성 검증 실패)
```json
도구: apply
인자:
{
  "payload": {
    "name": "테스트",
    "email": "invalid-email",
    "role": "Developer",
    "time_per_week": 100
  }
}
```

**실행 방법**:
- Tools 탭 → `apply` 선택
- Arguments 필드에 위 JSON 입력
- Execute

**통과 기준**:
- ✅ `{"ok": false, "error": [...]}`
- ✅ 에러 메시지에 이메일 형식 또는 시간 범위 오류 표시

---

### 2. Resources 테스트

#### Test 2.1: `roles://openings`
```
리소스: roles://openings
예상 결과: 모집 역할 목록 (Vision Engineer, LLM Engineer 등)
```

**실행 방법**:
- Resources 탭 → `roles://openings` 선택 → Read

**통과 기준**: ✅ 모집 역할 5개 표시

---

#### Test 2.2: `event://timeline`
```
리소스: event://timeline
예상 결과: 대회 일정 (Phase 1~4)
```

**실행 방법**:
- Resources 탭 → `event://timeline` 선택 → Read

**통과 기준**: ✅ Phase 1~4 일정 표시

---

### 3. Prompts 테스트

#### Test 3.1: `intro_template`
```
프롬프트: intro_template
인자: {"role": "Vision Engineer"}
예상 결과: 역할별 자기소개 양식
```

**실행 방법**:
- Prompts 탭 → `intro_template` 선택
- Arguments: `{"role": "Vision Engineer"}`
- Execute

**통과 기준**: ✅ Vision Engineer용 자기소개 양식 표시

---

## 📊 저장된 데이터 확인

### 지원서 파일 확인
```bash
cat data/applicants.jsonl
```

**통과 기준**:
- ✅ JSON Lines 형식
- ✅ 각 줄에 timestamp, name, email 등 필드 포함
- ✅ Test 1.3에서 제출한 지원서 포함

---

## 🚨 예상되는 문제 및 해결

### 문제 1: 401 Unauthorized
**증상**: 연결 시 401 오류

**해결**:
1. Authorization 헤더 확인
2. Bearer 토큰 앞에 공백 없는지 확인
3. `.env` 파일의 `MCP_API_KEY`와 일치하는지 확인

---

### 문제 2: Connection Failed
**증상**: Inspector에서 연결 실패

**해결**:
1. 서버 실행 확인: `curl http://localhost:8080/healthz`
2. 포트 8080이 사용 중인지 확인: `lsof -i:8080`
3. URL에 `http://` 포함되었는지 확인

---

### 문제 3: 지원서가 저장되지 않음
**증상**: apply 성공했지만 파일이 없음

**해결**:
1. `data/` 디렉토리 존재 확인
2. 쓰기 권한 확인
3. 서버 로그 확인

---

## ✅ 테스트 결과 기록

### Tools
- [ ] `ping` - 정상
- [ ] `faq` - 정상
- [ ] `apply` (정상) - 정상
- [ ] `apply` (검증 실패) - 정상

### Resources
- [ ] `roles://openings` - 정상
- [ ] `event://timeline` - 정상

### Prompts
- [ ] `intro_template` - 정상

### 데이터 저장
- [ ] `data/applicants.jsonl` 생성 - 정상
- [ ] 지원서 내용 확인 - 정상

---

## 🎉 다음 단계

테스트 완료 후:

1. **Slack 웹훅 재설정** (선택)
2. **GCP Cloud Run 배포**
3. **프로덕션 테스트**
4. **게시판 공지 작성**

---

## 📝 테스트 완료 보고서

테스트 완료 후 아래 정보를 기록:

```
테스트 일시: _______________
테스트 환경: macOS / Linux / Windows
MCP Inspector 버전: _______________

결과:
- Tools: ___/4 통과
- Resources: ___/2 통과
- Prompts: ___/1 통과
- 데이터 저장: ___/2 통과

총점: ___/9

이슈:
(발견된 문제 기록)

```
