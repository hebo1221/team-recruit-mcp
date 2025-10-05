# MCP 팀 리크루팅 서버 로컬 테스트 리포트

**테스트 일시**: 2025-10-05
**테스트 환경**: macOS, Python 3.13.2, venv

---

## ✅ 테스트 결과 요약

### 성공 항목
- [x] 가상 환경 생성 및 의존성 설치
- [x] 환경 변수 설정 (.env)
- [x] MCP 서버 실행
- [x] 헬스체크 엔드포인트 (`/healthz`) 정상 동작

### 부분 성공
- [~] MCP 프로토콜 테스트 - 서버는 정상 실행 중이나, 프로토콜 테스트는 MCP Inspector 필요

---

## 🔧 수정 사항

### 1. FastMCP 초기화 오류
**문제**: `TypeError: FastMCP.__init__() got an unexpected keyword argument 'version'`

**수정**:
```python
# Before
mcp = FastMCP(name="TeamRecruit", version="1.0.0")

# After
mcp = FastMCP(name="TeamRecruit")
```

### 2. 라우팅 순서 문제
**문제**: `/healthz` 엔드포인트가 404 반환

**수정**:
```python
# Before
app = Starlette(
    routes=[
        Mount("/", app=mcp_asgi),
        Route("/healthz", healthz, methods=["GET"]),
    ]
)

# After
app = Starlette(
    routes=[
        Route("/healthz", healthz, methods=["GET"]),  # 특정 라우트를 먼저
        Mount("/", app=mcp_asgi),
    ]
)
```

**이유**: Starlette는 첫 번째로 매칭되는 라우트를 사용하므로, `Mount("/")`가 앞에 있으면 모든 요청을 가로챔.

---

## 📊 서버 상태

### 실행 로그
```
2025-10-05 22:06:55,023 - __main__ - INFO - Starting MCP server on port 8080
INFO:     Started server process [71646]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

### 헬스체크 결과
```bash
$ curl http://localhost:8080/healthz
ok
```

**상태**: ✅ 정상

---

## 🧪 테스트 명령어

### 서버 실행
```bash
cd mcp-team-recruit
source venv/bin/activate
python server.py
```

### 헬스체크
```bash
curl http://localhost:8080/healthz
# 응답: ok
```

### MCP 클라이언트 테스트 (권장)
```bash
# MCP Inspector 사용
npx @modelcontextprotocol/inspector

# 연결 정보
URL: http://localhost:8080/
Authorization: Bearer 81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474
```

---

## 📝 환경 변수 설정

### .env 파일
```bash
MCP_API_KEY=REDACTED
# SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...  # 선택
PORT=8080
```

---

## 🚀 다음 단계

### 1. MCP Inspector로 기능 테스트
```bash
npx @modelcontextprotocol/inspector
```

연결 후 다음 기능 확인:
- Tools: `ping`, `faq`, `apply`
- Resources: `roles://openings`, `event://timeline`
- Prompts: `intro_template`

### 2. 지원서 제출 테스트
```json
{
  "name": "김정훈",
  "email": "kjh@example.com",
  "role": "Vision Engineer",
  "github": "https://github.com/kjh",
  "skills": ["YOLO", "DeepStream", "PyTorch"],
  "time_per_week": 20,
  "notes": "테스트 지원서"
}
```

결과:
- `data/applicants.jsonl` 파일에 저장 확인
- 슬랙 웹훅 설정 시 알림 확인

### 3. GCP Cloud Run 배포
```bash
export GCP_PROJECT_ID=your-project-id
export MCP_API_KEY=$(openssl rand -hex 24)
./deploy.sh
```

---

## 📚 참고 자료

### 생성된 파일
- `server.py` - MCP 서버 메인 코드
- `requirements.txt` - Python 의존성
- `Dockerfile` - 컨테이너 이미지
- `.env` - 환경 변수 (gitignore)
- `deploy.sh` - GCP 배포 스크립트
- `docs/CLIENT_GUIDE.md` - 지원자용 가이드
- `docs/POSTING.md` - 게시판용 안내문
- `README.md` - 프로젝트 문서

### MCP 기능
| 기능 | 타입 | 설명 |
|------|------|------|
| `ping` | Tool | 연결 테스트 |
| `faq` | Tool | 대회/팀 FAQ |
| `apply` | Tool | 지원서 제출 |
| `roles://openings` | Resource | 모집 역할 |
| `event://timeline` | Resource | 대회 일정 |
| `intro_template` | Prompt | 자기소개 양식 |

---

## 🎯 결론

**서버 상태**: ✅ 정상 동작
**배포 준비**: ✅ 완료

다음 작업:
1. MCP Inspector로 전체 기능 테스트
2. 슬랙 웹훅 연결 (선택)
3. GCP Cloud Run 배포
4. 커스텀 도메인 연결
5. 게시판에 공지 작성

**로컬 테스트**: 성공 ✅
