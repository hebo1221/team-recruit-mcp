# MCP 팀 리크루팅 서버

**Model Context Protocol(MCP)**를 활용한 대회 팀원 모집 시스템

지원자가 MCP 프로토콜을 통해 구조화된 지원서를 제출하고, 팀 정보를 조회할 수 있는 원격 MCP 서버입니다.

---

## 🎯 주요 특징

- ✅ **표준화된 지원서**: Pydantic 스키마 검증으로 일관된 데이터 품질
- ✅ **즉시 알림**: 슬랙 웹훅을 통한 실시간 지원서 알림
- ✅ **영구 저장**: JSONL 파일 기반 지원서 저장
- ✅ **원격 접속**: Streamable HTTP를 통한 안전한 원격 연결
- ✅ **Bearer 인증**: API 키 기반 접근 제어
- ✅ **GCP 최적화**: Cloud Run 서울 리전 배포 스크립트 포함

---

## 📂 프로젝트 구조

```
mcp-team-recruit/
├── server.py              # MCP 서버 메인 코드
├── requirements.txt       # Python 패키지
├── Dockerfile            # 컨테이너 이미지
├── .dockerignore
├── .env.example          # 환경 변수 템플릿
├── deploy.sh             # GCP Cloud Run 배포 스크립트
├── data/                 # 지원서 저장 디렉토리 (gitignore)
│   └── applicants.jsonl
├── docs/
│   ├── CLIENT_GUIDE.md   # 지원자용 연결 가이드
│   └── POSTING.md        # 게시판용 안내문 (복붙용)
└── README.md
```

---

## 🚀 빠른 시작

### 1. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# API 키 생성
openssl rand -hex 24

# .env 파일 편집
# MCP_API_KEY=<생성된_키>
# SLACK_WEBHOOK_URL=<슬랙_웹훅_URL> (선택)
```

### 2. 로컬 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python server.py

# 또는 uvicorn으로 실행
uvicorn server:app --reload --port 8080
```

### 3. 헬스체크

```bash
curl http://localhost:8080/healthz
# 응답: ok
```

---

## ☁️ GCP Cloud Run 배포

### 사전 준비
- GCP 프로젝트 생성
- gcloud CLI 설치 및 인증

### 배포 실행

```bash
# 환경 변수 설정
export GCP_PROJECT_ID=my-project-id
export MCP_API_KEY=$(openssl rand -hex 24)
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...  # 선택

# 배포 스크립트 실행
./deploy.sh
```

배포가 완료되면 서비스 URL이 출력됩니다:
```
서비스 URL: https://mcp-team-recruit-xxxxx-an.a.run.app
```

### 커스텀 도메인 연결 (선택)

1. Cloud Run 콘솔에서 서비스 선택
2. "도메인 매핑" 탭 → "도메인 추가"
3. `mcp.your-domain.com` 입력
4. DNS 설정에 따라 레코드 추가

---

## 🛠️ MCP 서버 기능

### Tools

#### `team.ping()`
연결 테스트

```python
team.ping()
# 응답: "pong ✅"
```

#### `team.faq()`
대회 및 팀 FAQ 조회

```python
team.faq()
```

#### `team.apply(payload)`
지원서 제출

```python
team.apply({
    "name": "김정훈",
    "email": "kjh@example.com",
    "role": "Vision Engineer",
    "github": "https://github.com/kjh",
    "skills": ["YOLO", "DeepStream", "PyTorch"],
    "time_per_week": 20,
    "notes": "도로교통 영상 인식 프로젝트 3건 경험"
})
```

**스키마**:
- `name` (필수): 이름 (2-50자)
- `email` (필수): 이메일 (유효한 형식)
- `role` (필수): 희망 역할
- `time_per_week` (필수): 주당 투입 시간 (1-80)
- `github` (선택): GitHub URL
- `portfolio` (선택): 포트폴리오 URL
- `skills` (선택): 스킬 배열
- `notes` (선택): 추가 메시지 (최대 1000자)

### Resources

#### `roles://openings`
모집 역할 및 요구사항 조회

#### `event://timeline`
대회 일정 조회

### Prompts

#### `intro_template(role)`
역할별 자기소개 양식 템플릿

```python
intro_template(role="Vision Engineer")
```

---

## 👥 지원자 안내

### MCP 클라이언트 연결

지원자는 다음 클라이언트 중 하나로 연결할 수 있습니다:

1. **Claude Desktop** (권장)
   - Settings → Connectors → Add custom connector
   - URL: `https://mcp.your-domain.com/`
   - Header: `Authorization: Bearer <토큰>`

2. **MCP Inspector**
   ```bash
   npx @modelcontextprotocol/inspector
   ```

3. **기타 호환 클라이언트**
   - Cursor
   - Amazon Q CLI

자세한 연결 방법은 [CLIENT_GUIDE.md](docs/CLIENT_GUIDE.md)를 참고하세요.

---

## 📊 데이터 관리

### 지원서 저장 형식

지원서는 `data/applicants.jsonl` 파일에 JSONL 형식으로 저장됩니다:

```jsonl
{"timestamp": "2025-01-01T12:00:00Z", "name": "김정훈", "email": "kjh@example.com", ...}
{"timestamp": "2025-01-01T13:00:00Z", "name": "이영희", "email": "yhlee@example.com", ...}
```

### 슬랙 알림

지원서 제출 시 슬랙 채널로 자동 알림이 전송됩니다:

- 이름, 역할, 이메일, 주당 시간
- 보유 스킬
- GitHub 링크
- 추가 메시지

---

## 🔒 보안

### 인증
- Bearer 토큰 기반 인증
- 환경 변수로 API 키 관리
- 헬스체크 엔드포인트는 무인증 허용

### 토큰 관리
```bash
# 새 토큰 생성
openssl rand -hex 24

# Cloud Run 환경 변수 업데이트
gcloud run services update mcp-team-recruit \
  --region asia-northeast3 \
  --set-env-vars MCP_API_KEY=<새_토큰>
```

### 레이트 리밋 (선택)
Cloudflare 또는 GCP Load Balancer를 통해 레이트 리밋을 설정할 수 있습니다.

---

## 🧪 테스트

### 로컬 테스트

```bash
# 헬스체크
curl http://localhost:8080/healthz

# ping (인증 필요)
curl -X POST http://localhost:8080/ \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"method":"tools/call","params":{"name":"team.ping"}}'
```

### MCP Inspector로 테스트

```bash
npx @modelcontextprotocol/inspector
```

URL과 토큰 입력 후 Tools 탭에서 각 기능을 테스트하세요.

---

## 📝 게시판 안내문

[docs/POSTING.md](docs/POSTING.md)에서 팀 빌딩 게시판용 안내문을 복사할 수 있습니다.

**사용 전 수정 필요 항목**:
- 실제 MCP 서버 URL
- 토큰 발급 이메일/폼 링크
- 연락처 정보

---

## 🛠️ 개발

### 의존성 추가

```bash
# requirements.txt 편집
echo "new-package>=1.0.0" >> requirements.txt

# 설치
pip install -r requirements.txt
```

### 서버 코드 수정

`server.py`를 편집한 후:

```bash
# 로컬에서 테스트
uvicorn server:app --reload

# 재배포
./deploy.sh
```

---

## 🐛 트러블슈팅

### 배포 실패

**증상**: `deploy.sh` 실행 시 오류

**해결**:
1. `GCP_PROJECT_ID` 환경 변수 확인
2. gcloud 인증 상태 확인: `gcloud auth list`
3. 프로젝트 설정 확인: `gcloud config get-value project`

### 슬랙 알림이 안 옴

**증상**: 지원서 제출은 성공하지만 슬랙에 알림이 없음

**해결**:
1. `SLACK_WEBHOOK_URL` 환경 변수 확인
2. 웹훅 URL이 유효한지 테스트:
   ```bash
   curl -X POST $SLACK_WEBHOOK_URL \
     -H 'Content-Type: application/json' \
     -d '{"text":"테스트 메시지"}'
   ```

### 401 Unauthorized

**증상**: 클라이언트 연결 시 401 오류

**해결**:
1. `Authorization` 헤더 형식 확인: `Bearer <토큰>`
2. 토큰이 서버의 `MCP_API_KEY`와 일치하는지 확인
3. 토큰 앞뒤 공백 제거

---

## 📚 참고 자료

- [Model Context Protocol 공식 문서](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [GCP Cloud Run 문서](https://cloud.google.com/run/docs)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)

---

## 📄 라이선스

MIT License

---

## 🤝 기여

이슈 및 PR 환영합니다!

---

## 📧 문의

- **이메일**: recruit@example.com
- **GitHub**: [링크]

---

**🎉 성공적인 팀 빌딩을 응원합니다!**
