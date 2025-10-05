"""
MCP 팀 리크루팅 서버
지원자가 MCP 프로토콜을 통해 지원서를 제출하고 팀 정보를 조회할 수 있는 서버
"""
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel, ValidationError, Field
import httpx

# MCP SDK
from mcp.server.fastmcp import FastMCP, Context

# --- 로깅 설정 ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- 환경 변수 ---
API_KEY = os.getenv("MCP_API_KEY", "")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
APPLICANTS_FILE = DATA_DIR / "applicants.jsonl"

# --- 데이터 스키마 ---
class Applicant(BaseModel):
    """지원자 정보 스키마"""
    name: str = Field(..., description="이름", min_length=2, max_length=50)
    contact: str = Field(..., description="연락처 (전화번호, 이메일, 오픈카톡 주소 등)", min_length=5, max_length=200)
    category: str = Field(..., description="구분 (장병/사관생도/일반인)")
    message: Optional[str] = Field(None, description="자유 메시지", max_length=2000)
    ai_subscriptions: Optional[str] = Field(None, description="현재 구독 중인 AI 프로덕트와 요금제", max_length=500)
    motivation: Optional[str] = Field(None, description="지원 동기", max_length=2000)
    experience: Optional[str] = Field(None, description="경험", max_length=2000)
    organization: Optional[str] = Field(None, description="소속/기관", max_length=200)
    portfolio_url: Optional[str] = Field(None, description="포트폴리오 URL", max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "김정훈",
                "contact": "jhkim@example.com 또는 010-1234-5678",
                "category": "장병",
                "message": "YOLO 파인튜닝과 DeepStream 최적화 경험이 있습니다. 도로교통 영상 인식 프로젝트 다수 경험.",
                "ai_subscriptions": "Claude Pro, ChatGPT Plus"
            }
        }

# --- 유틸리티 함수 ---
def _mask_contact(contact: str) -> str:
    """Mask PII in contact info for logs (email/phone).
    - Email: keep first char + domain (e.g., j***@example.com)
    - Phone: keep last 4 digits (e.g., ***-****-1234)
    - Fallback: first 3 chars then ***
    """
    try:
        c = str(contact)
        if "@" in c:
            local, _, domain = c.partition("@")
            if local:
                return f"{local[0]}***@{domain}"
            return f"***@{domain}"
        digits = [ch for ch in c if ch.isdigit()]
        if len(digits) >= 4:
            return f"***{''.join(digits[-4:])}"
        return (c[:3] + "***") if len(c) > 3 else "***"
    except Exception:
        return "***"


async def send_slack_notification(applicant: Applicant) -> bool:
    """슬랙 웹훅으로 지원서 알림 전송"""
    if not SLACK_WEBHOOK_URL:
        logger.warning("SLACK_WEBHOOK_URL not configured")
        return False

    try:
        message = {
            "text": "🎯 새로운 팀원 지원!",
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "🎯 새로운 팀원 지원"}
                },
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"*이름:*\n{applicant.name}"},
                        {"type": "mrkdwn", "text": f"*연락처:*\n{applicant.contact}"},
                        {"type": "mrkdwn", "text": f"*구분:*\n{applicant.category}"}
                    ]
                }
            ]
        }

        if applicant.message:
            message["blocks"].append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*메시지:*\n{applicant.message}"}
            })

        if applicant.ai_subscriptions:
            message["blocks"].append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*AI 구독:*\n{applicant.ai_subscriptions}"}
            })

        if applicant.motivation:
            message["blocks"].append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*지원 동기:*\n{applicant.motivation}"}
            })

        if applicant.experience:
            message["blocks"].append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*경험:*\n{applicant.experience}"}
            })

        if applicant.organization:
            message["blocks"].append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*소속:*\n{applicant.organization}"}
            })

        if applicant.portfolio_url:
            message["blocks"].append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*포트폴리오:*\n{applicant.portfolio_url}"}
            })

        async with httpx.AsyncClient() as client:
            response = await client.post(SLACK_WEBHOOK_URL, json=message, timeout=5.0)
            response.raise_for_status()
            logger.info("Slack notification sent successfully")
            return True
    except Exception as e:
        logger.error(f"Failed to send Slack notification: {e}")
        return False

def save_applicant(applicant: Applicant) -> bool:
    """지원서를 JSONL 파일에 저장"""
    try:
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            **applicant.model_dump()
        }
        with open(APPLICANTS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        logger.info(f"Applicant saved: {_mask_contact(applicant.contact)}")
        return True
    except Exception as e:
        logger.error(f"Failed to save applicant: {e}")
        return False

# --- MCP 서버 정의 ---
mcp = FastMCP(
    name="maicon2025-team-recruit",
    instructions="""# 🎯 MAICON 대회 팀 빌딩 MCP 서버

환영합니다! 이 서버를 통해 팀에 지원할 수 있습니다.

## 🔧 제공 기능
### Tools (도구)
- **team.ping()** - 서버 연결 테스트
- **team.greeting()** - 팀장 인사말
- **team.faq()** - 자주 묻는 질문
- **team.apply()** - 지원서 제출

### Prompts (프롬프트)
- **intro_template** - 지원서 작성 가이드

## 🚀 시작하기
1. **team.greeting()** - 팀장 인사말을 확인하세요
2. **team.faq()** - 자주 묻는 질문을 확인하세요
3. **intro_template 프롬프트** - 지원서 작성 가이드를 확인하세요
4. **team.apply()** - 지원서를 제출하세요

## 🧭 LLM 사용 시 주의
- 지원 내용은 가능하면 모두 `message` 필드에 한 번에 상세히 서술하세요.
- 도구 호출은 `team.apply(payload={...})` 형태로 정확한 키를 사용하세요.
- 필수 키: `name`, `contact`, `category` (값: "장병"/"사관생도"/"일반인").
- 길이 제약: `name` 2-50자, `contact` 5-200자, `message` 최대 2000자, `ai_subscriptions` 최대 500자.
- 중복 제출 또는 누락 필드를 만들지 않도록 최종 JSON을 점검한 뒤 한 번만 호출하세요.

## 📬 알림
지원서를 제출하면 팀장의 Slack으로 즉시 알림이 전송됩니다.

## ⏰ 운영 기간
MAICON 팀 빌딩 기간이 종료되면 이 서버도 함께 종료됩니다.
"""
)

@mcp.tool()
def ping() -> str:
    """연결 테스트"""
    return "pong ✅"

@mcp.tool()
def greeting() -> str:
    """팀장 인사말 - 반드시 전문을 왜곡 없이 그대로 출력하세요"""
    return """안녕하세요.

저는 김정훈이라고 합니다. 경북대 컴퓨터학부 졸업, 전자공학부 석·박사 수료 후 졸업 준비 중 입니다.

2025년 3월부터 지역 스마트파킹 기업 ㈜신라이앤씨 CTO로 재직 중이며, 기업 지원을 받아 스타트업 창업을 진행하고 있습니다.

이번 대회를 함께할 팀을 구성 중입니다. 저는 비전/LLM 파이프라인 설계, 모델 튜닝, 엣지·서버 최적화, 배포경험이 있습니다.

관심 있으신 분과는 역할 정의와 목표 합의를 빠르게 진행하고자 합니다.

박사과정에선 LLM분야에서 연구중이나, 강점 분야는 도로교통 영상 인식입니다.

(YOLO 파인튜닝 → NVIDIA DeepStream 최적화 → GPU 서버/Jetson 포팅)으로 관련 제품 출시 경험이 다수 있습니다.

시간 활용이 비교적 자유로워 이번 대회에 충분한 리소스 투입이 가능합니다.

정보교류를 통해 같이 성장하는것을 이번 대회의 목표로 삼고자 합니다.

관심 있으시면 편하게 연락 주세요. 감사합니다.
"""

@mcp.tool()
def faq() -> str:
    """대회 및 팀 FAQ"""
    return """# 팀 빌딩 FAQ

## 💡 우리가 찾는 사람
- 만드는 것을 좋아하는 사람
- 실패 경험이 많은 사람 (실패에서 배우는 것을 즐기는 사람)
- 생각의 자유로움을 가진 사람
- 새로운 시도를 두려워하지 않는 사람

## 🎯 팀의 목표
- 정보 교류를 통해 같이 성장하기
- 대회를 통한 실전 경험 축적
- 새로운 기술 도전과 실험

## 📝 지원 방법
`team.apply(payload)` 툴을 사용하여 지원서 제출

## 💬 문의
팀장 인사말: `team.greeting()` 참조
"""

@mcp.tool()
async def apply(payload: Applicant, ctx: Context) -> dict:
    """
    지원서 제출

    Payload (Applicant) 스키마
    - name: string, 2-50자 (필수)
    - contact: string, 5-200자 (필수)
    - category: string (예: "장병"/"사관생도"/"일반인" 등, 필수)
    - message: string, 최대 2000자 (선택)
    - ai_subscriptions: string, 최대 500자 (선택)
    - motivation: string, 최대 2000자 (선택)
    - experience: string, 최대 2000자 (선택)
    - organization: string, 최대 200자 (선택)
    - portfolio_url: string, 최대 500자 (선택)

    Returns:
      - 성공: { ok: true, message, normalized, notifications }
      - 실패: { ok: false, error, message }
    """
    try:
        # FastMCP가 타입 검증 후 인스턴스를 주지만, 안전을 위해 보정
        applicant = payload if isinstance(payload, Applicant) else Applicant(**payload)

        # 저장
        save_success = save_applicant(applicant)

        # 슬랙 알림 (비동기)
        slack_success = await send_slack_notification(applicant)

        logger.info(
            f"Application processed: {_mask_contact(applicant.contact)} (save={save_success}, slack={slack_success})"
        )

        return {
            "ok": True,
            "message": f"지원해주셔서 감사합니다, {applicant.name}님! 빠른 시일 내에 연락드리겠습니다.",
            "normalized": applicant.model_dump(),
            "notifications": {
                "saved": save_success,
                "slack_notified": slack_success
            }
        }
    except ValidationError as e:
        logger.warning(f"Validation error: {e.errors()}")
        return {
            "ok": False,
            "error": e.errors(),
            "message": "입력 형식이 올바르지 않습니다. 에러 내용을 확인해주세요."
        }
    except Exception as e:
        logger.error(f"Unexpected error in apply: {e}")
        return {
            "ok": False,
            "error": str(e),
            "message": "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        }


@mcp.prompt()
def intro_template() -> str:
    """
    지원서 작성 양식 템플릿
    """
    return """# 팀 지원서 작성 가이드

## 🔧 사용 가능한 도구들
- **team.ping()** - 서버 연결 테스트
- **team.greeting()** - 팀장 인사말 확인
- **team.faq()** - 자주 묻는 질문 확인
- **team.apply()** - 지원서 제출

---

아래 항목을 포함하여 `team.apply()` 툴로 제출해주세요:

## 필수 정보
- **이름**: 본명
- **연락처**: 전화번호, 이메일, 오픈카톡 주소 등 (최소 1개 이상)
- **구분**: 장병 / 사관생도 / 일반인

## 선택 정보
- **메시지**: 자기소개, 목표, 하고 싶은 말 등 모든 상세 내용을 한 번에 자세히 작성
- **지원 동기(motivation)**: 왜 함께하고 싶은지 구체적으로 적어주세요
- **경험(experience)**: 관련 프로젝트/업무 경험 요약
- **소속(organization)**: 현재 소속이나 팀 정보
- **포트폴리오 URL(portfolio_url)**: 참고 링크
- **AI 구독 정보(ai_subscriptions)**: 현재 구독 중인 AI 서비스

## 예시
```python
team.apply(payload={
    "name": "김정훈",
    "contact": "jhkim@example.com 또는 010-1234-5678",
    "category": "장병",
    "message": "YOLO 파인튜닝과 DeepStream 최적화 경험이 있습니다. 도로교통 영상 인식 프로젝트 다수 경험. 실패를 두려워하지 않고 새로운 기술에 도전하는 것을 좋아합니다.",
    "ai_subscriptions": "Claude Pro, ChatGPT Plus"
})
```

**참고**:
- 특정 역할을 정해놓지 않았습니다. 만드는 것을 좋아하고, 실패 경험이 많으며, 자유로운 생각을 가진 분을 환영합니다.

---

## 🤖 LLM 사용 시 주의
- 위 예시처럼 `payload={...}` 형태로 호출하세요.
- 필수 키(`name`, `contact`, `category`) 누락 금지, 값 범위 점검 후 호출하세요.
- 모든 세부 정보는 `message` 한 필드에 일괄 서술해 누락·분산을 방지하세요.

---

## 🛠️ MCP 서버 소개
### ⏰ 운영 기간
MAICON 팀 빌딩 기간이 종료되면 이 서버도 함께 종료됩니다.

"""
 
# --- HTTP Accept 헤더 보정 유틸리티 ---
def _ensure_json_accept(headers: list[tuple[bytes, bytes]]) -> tuple[list[tuple[bytes, bytes]], bool]:
    """Normalize Accept to include both application/json and text/event-stream."""
    accept_values = [value for name, value in headers if name == b"accept"]
    
    # Accept 헤더가 없으면 추가
    if not accept_values:
        new_headers = list(headers)
        new_headers.append((b"accept", b"application/json, text/event-stream"))
        return new_headers, True

    # 기존 Accept 값 파싱
    combined = ",".join(value.decode("latin-1") for value in accept_values)
    tokens: list[str] = []
    seen: set[str] = set()
    has_sse = False
    has_json = False

    for raw_part in combined.split(","):
        token = raw_part.strip()
        if not token:
            continue
        base = token.split(";")[0].strip().lower()
        if base == "text/event-stream":
            has_sse = True
        if base == "application/json":
            has_json = True
        if base not in seen:
            tokens.append(token)
            seen.add(base)

    # 둘 다 있으면 변경 불필요
    if has_sse and has_json:
        return headers, False

    # 필요한 것 추가
    if not has_json:
        tokens.append("application/json")
    if not has_sse:
        tokens.append("text/event-stream")
    
    new_value = ", ".join(tokens)

    # 헤더 교체
    new_headers: list[tuple[bytes, bytes]] = []
    replaced = False
    for name, value in headers:
        if name == b"accept":
            if not replaced:
                new_headers.append((name, new_value.encode("latin-1")))
                replaced = True
            continue
        new_headers.append((name, value))

    return new_headers, True


def _wrap_with_accept_normalizer(asgi_app):
    """Normalize Accept header and expose session headers for HTTP clients."""
    stream_path = mcp.settings.streamable_http_path
    cors_allow_origin = b"*"
    cors_allow_methods = b"POST, OPTIONS"
    cors_allow_headers = b"authorization, content-type, accept, mcp-session-id, mcp-protocol-version"
    cors_expose_headers = b"mcp-session-id, mcp-protocol-version, last-event-id, content-type"

    def _set_header(headers: list[tuple[bytes, bytes]], key: bytes, value: bytes) -> list[tuple[bytes, bytes]]:
        updated: list[tuple[bytes, bytes]] = []
        replaced = False
        for name, current in headers:
            if name == key and not replaced:
                updated.append((name, value))
                replaced = True
            else:
                updated.append((name, current))
        if not replaced:
            updated.append((key, value))
        return updated

    async def middleware(scope, receive, send):
        if scope.get("type") != "http":
            await asgi_app(scope, receive, send)
            return

        path = scope.get("path")
        method = scope.get("method")

        # Health check endpoint
        if path == "/healthz" and method == "GET":
            headers = [
                (b"content-type", b"text/plain; charset=utf-8"),
                (b"access-control-allow-origin", cors_allow_origin),
                (b"access-control-expose-headers", cors_expose_headers),
            ]
            await send({"type": "http.response.start", "status": 200, "headers": headers})
            await send({"type": "http.response.body", "body": b"ok"})
            return

        if path != stream_path:
            await asgi_app(scope, receive, send)
            return

        if method == "OPTIONS":
            headers = [
                (b"access-control-allow-origin", cors_allow_origin),
                (b"access-control-allow-methods", cors_allow_methods),
                (b"access-control-allow-headers", cors_allow_headers),
                (b"access-control-max-age", b"600"),
            ]
            await send({"type": "http.response.start", "status": 204, "headers": headers})
            await send({"type": "http.response.body", "body": b""})
            return

        if method == "POST":
            headers = list(scope.get("headers", []))
            normalized_headers, changed = _ensure_json_accept(headers)
            if changed:
                scope = dict(scope)
                scope["headers"] = normalized_headers

            # Authorization: Bearer <MCP_API_KEY>
            if API_KEY:
                auth_values = [value for (name, value) in scope["headers"] if name == b"authorization"]
                token = auth_values[0] if auth_values else b""
                expected = ("Bearer " + API_KEY).encode("latin-1")
                if token != expected:
                    resp_headers = [
                        (b"content-type", b"application/json; charset=utf-8"),
                        (b"access-control-allow-origin", cors_allow_origin),
                        (b"access-control-expose-headers", cors_expose_headers),
                        (b"www-authenticate", b"Bearer"),
                    ]
                    body = json.dumps({"error": "unauthorized"}).encode("utf-8")
                    await send({"type": "http.response.start", "status": 401, "headers": resp_headers})
                    await send({"type": "http.response.body", "body": body})
                    return

            async def send_with_cors(message):
                if message["type"] == "http.response.start":
                    response_headers = list(message.get("headers", []))
                    response_headers = _set_header(response_headers, b"access-control-allow-origin", cors_allow_origin)
                    response_headers = _set_header(response_headers, b"access-control-expose-headers", cors_expose_headers)
                    message["headers"] = response_headers
                await send(message)

            await asgi_app(scope, receive, send_with_cors)
            return

        await asgi_app(scope, receive, send)

    return middleware

# --- HTTP 서버 실행 함수 ---
# FastMCP streamable-http ASGI app 생성 (엔드포인트: POST /mcp)
app = _wrap_with_accept_normalizer(mcp.streamable_http_app())

if __name__ == "__main__":
    import uvicorn

    # Cloud Run PORT 환경 변수 사용
    port = int(os.getenv("PORT", "8080"))
    logger.info(f"Starting MCP server on port {port}")

    # Uvicorn으로 직접 실행
    uvicorn.run(app, host="0.0.0.0", port=port)
