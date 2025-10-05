#!/usr/bin/env python3
"""
전체 통합 테스트: 지원서 제출 → 저장 → Slack 알림
"""
import sys
import os
import asyncio
import json

# 환경 변수 설정
os.environ['SLACK_WEBHOOK_URL'] = 'https://example.com/slack-webhook'
os.environ['MCP_API_KEY'] = '81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474'

sys.path.insert(0, os.path.dirname(__file__))

from server import Applicant, save_applicant, send_slack_notification
from pathlib import Path

async def test_full_workflow():
    """전체 워크플로우 테스트"""
    print("\n" + "=" * 70)
    print("전체 통합 테스트: 지원서 제출 → 저장 → Slack 알림")
    print("=" * 70)

    # 테스트 지원자
    applicant = Applicant(
        name="최종 통합 테스트",
        contact="integration_test@example.com",
        category="장병",
        message="전체 통합 테스트: 지원서 저장 및 Slack 알림 검증",
        ai_subscriptions="Claude Pro"
    )

    print(f"\n1️⃣  지원자 정보:")
    print(f"   이름: {applicant.name}")
    print(f"   연락처: {applicant.contact}")
    print(f"   구분: {applicant.category}")
    if applicant.ai_subscriptions:
        print(f"   AI 구독: {applicant.ai_subscriptions}")

    # Step 1: 파일 저장
    print(f"\n2️⃣  파일 저장 중...")
    save_success = save_applicant(applicant)

    if save_success:
        print("   ✅ 파일 저장 성공")

        # 저장된 파일 확인
        data_file = Path(__file__).parent / "data" / "applicants.jsonl"
        with open(data_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_entry = json.loads(lines[-1])
            print(f"   ✅ 마지막 저장 항목:")
            print(f"      - 이름: {last_entry['name']}")
            print(f"      - 연락처: {last_entry['contact']}")
            print(f"      - 타임스탬프: {last_entry['timestamp']}")
    else:
        print("   ❌ 파일 저장 실패")
        return False

    # Step 2: Slack 알림
    print(f"\n3️⃣  Slack 알림 전송 중...")
    slack_success = await send_slack_notification(applicant)

    if slack_success:
        print("   ✅ Slack 알림 전송 성공")
        print("   📱 Slack 채널에서 확인하세요!")
    else:
        print("   ❌ Slack 알림 전송 실패")

    # 최종 결과
    print("\n" + "=" * 70)
    if save_success and slack_success:
        print("🎉 전체 통합 테스트 성공!")
        print("\n✅ 확인 사항:")
        print("   1. data/applicants.jsonl에 지원서 저장됨")
        print("   2. Slack 채널에 알림 도착함")
        print("\n💡 이제 GCP Cloud Run 배포 준비가 완료되었습니다!")
    else:
        print("❌ 일부 기능 실패")
        print(f"   - 파일 저장: {'✅' if save_success else '❌'}")
        print(f"   - Slack 알림: {'✅' if slack_success else '❌'}")
    print("=" * 70 + "\n")

    return save_success and slack_success

if __name__ == "__main__":
    result = asyncio.run(test_full_workflow())
    sys.exit(0 if result else 1)
