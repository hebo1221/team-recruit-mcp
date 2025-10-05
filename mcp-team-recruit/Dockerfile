# MCP 팀 리크루팅 서버 Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 환경 변수 설정 (빌드 최적화)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY server.py .

# 데이터 디렉토리 생성
RUN mkdir -p /app/data

# 포트 설정 (Cloud Run은 환경변수로 주입)
ENV PORT=8080
EXPOSE 8080

# 서버 실행 (FastMCP streamable-http ASGI app)
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
