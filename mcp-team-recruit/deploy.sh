#!/bin/bash
# GCP Cloud Run 배포 자동화 스크립트

set -e  # 에러 시 즉시 종료

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# --- 설정 (필수) ---
PROJECT_ID="${GCP_PROJECT_ID:-}"
SERVICE_NAME="${SERVICE_NAME:-mcp-team-recruit}"
REGION="${GCP_REGION:-asia-northeast3}"  # 서울 리전
IMAGE_NAME="${IMAGE_NAME:-gcr.io/$PROJECT_ID/$SERVICE_NAME}"

# --- 환경 변수 확인 ---
echo -e "${YELLOW}=== 배포 설정 확인 ===${NC}"

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}오류: GCP_PROJECT_ID 환경 변수가 설정되지 않았습니다.${NC}"
    echo "예시: export GCP_PROJECT_ID=my-project-id"
    exit 1
fi

if [ -z "$MCP_API_KEY" ]; then
    echo -e "${YELLOW}경고: MCP_API_KEY 환경 변수가 설정되지 않았습니다.${NC}"
    echo "배포 후 Cloud Run 콘솔에서 수동으로 설정해야 합니다."
    echo "계속하려면 Enter를 누르세요 (취소: Ctrl+C)"
    read
fi

echo "프로젝트 ID: $PROJECT_ID"
echo "서비스명: $SERVICE_NAME"
echo "리전: $REGION"
echo "이미지: $IMAGE_NAME"
echo ""

# --- gcloud 인증 확인 ---
echo -e "${YELLOW}=== gcloud 인증 확인 ===${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}오류: gcloud 인증이 필요합니다.${NC}"
    echo "실행: gcloud auth login"
    exit 1
fi

# 프로젝트 설정
gcloud config set project "$PROJECT_ID"

# --- Docker 이미지 빌드 ---
echo -e "${YELLOW}=== Docker 이미지 빌드 ===${NC}"
docker build -t "$IMAGE_NAME:latest" .

# --- Container Registry 푸시 ---
echo -e "${YELLOW}=== Container Registry에 푸시 ===${NC}"

# Container Registry API 활성화 확인
gcloud services enable containerregistry.googleapis.com --project="$PROJECT_ID" 2>/dev/null || true

# Docker 인증 설정
gcloud auth configure-docker --quiet

docker push "$IMAGE_NAME:latest"

# --- Cloud Run 배포 ---
echo -e "${YELLOW}=== Cloud Run 배포 ===${NC}"

# Cloud Run API 활성화
gcloud services enable run.googleapis.com --project="$PROJECT_ID" 2>/dev/null || true

# 환경 변수 준비
ENV_VARS="PORT=8080"
if [ -n "$MCP_API_KEY" ]; then
    ENV_VARS="$ENV_VARS,MCP_API_KEY=$MCP_API_KEY"
fi
if [ -n "$SLACK_WEBHOOK_URL" ]; then
    ENV_VARS="$ENV_VARS,SLACK_WEBHOOK_URL=$SLACK_WEBHOOK_URL"
fi

# 배포
gcloud run deploy "$SERVICE_NAME" \
    --image "$IMAGE_NAME:latest" \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --set-env-vars "$ENV_VARS" \
    --max-instances 10 \
    --min-instances 0 \
    --cpu 1 \
    --memory 512Mi \
    --timeout 60s \
    --concurrency 80 \
    --port 8080

# --- 배포 완료 ---
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format="value(status.url)")

echo ""
echo -e "${GREEN}=== 배포 완료! ===${NC}"
echo -e "서비스 URL: ${GREEN}$SERVICE_URL${NC}"
echo ""
echo "헬스체크: curl $SERVICE_URL/healthz"
echo "MCP 연결: $SERVICE_URL (Authorization: Bearer <토큰>)"
echo ""

if [ -z "$MCP_API_KEY" ]; then
    echo -e "${YELLOW}⚠️  MCP_API_KEY를 아직 설정하지 않았습니다.${NC}"
    echo "Cloud Run 콘솔에서 환경 변수를 추가하세요:"
    echo "https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME/variables?project=$PROJECT_ID"
fi

echo ""
echo -e "${GREEN}다음 단계:${NC}"
echo "1. 커스텀 도메인 연결 (선택)"
echo "2. 토큰 생성: openssl rand -hex 24"
echo "3. 지원자에게 서비스 URL과 토큰 공유"
