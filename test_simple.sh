#!/bin/bash
# 간단한 cURL 테스트

API_KEY="81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474"
BASE_URL="http://localhost:8080"

echo "=== 헬스체크 ==="
curl -s "${BASE_URL}/healthz"
echo -e "\n"

echo "=== 인증 없이 접근 (401 예상) ==="
curl -s -X POST "${BASE_URL}/" \
  -H "Content-Type: application/json" \
  -d '{}'
echo -e "\n"

echo "=== 인증 포함 접근 ==="
curl -s -X POST "${BASE_URL}/" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
echo -e "\n"

echo "=== 테스트 완료 ==="
