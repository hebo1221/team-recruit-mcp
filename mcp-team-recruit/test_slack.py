#!/usr/bin/env python3
"""
Slack 웹훅 통합 테스트
"""
import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(__file__))

from server import Applicant, send_slack_notification
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

async def test_slack_notification():
    """Slack 알림 테스트"""
    print("\n=== Slack 웹훅 통합 테스트 ===\n")

    # 웹훅 URL 확인
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("❌ SLACK_WEBHOOK_URL 환경 변수가 설정되지 않았습니다.")
        return False

    print(f"✅ Slack 웹훅 URL: {webhook_url[:50]}...")

    # 테스트 지원자 생성
    test_applicant = Applicant(
        name="김정훈 (테스트)",
        contact="kjh@example.com",
        category="장병",
        message="도로교통 영상 인식 프로젝트 3건 경험. 이것은 Slack 알림 테스트입니다.",
        ai_subscriptions="Claude Pro"
    )

    print(f"\n📝 테스트 지원자 정보:")
    print(f"   이름: {test_applicant.name}")
    print(f"   연락처: {test_applicant.contact}")
    print(f"   구분: {test_applicant.category}")
    if test_applicant.ai_subscriptions:
        print(f"   AI 구독: {test_applicant.ai_subscriptions}")

    print("\n📤 Slack 알림 전송 중...")

    # Slack 알림 전송 (상세 에러 로깅)
    try:
        success = await send_slack_notification(test_applicant)

        if success:
            print("✅ Slack 알림 전송 성공!")
            print("\n📱 Slack 앱 또는 웹에서 알림을 확인하세요.")
            return True
        else:
            print("❌ Slack 알림 전송 실패")
            print("   - 웹훅 URL이 올바른지 확인하세요")
            print("   - 네트워크 연결을 확인하세요")
            return False
    except Exception as e:
        print(f"❌ 예외 발생: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MCP 팀 리크루팅 - Slack 웹훅 테스트")
    print("=" * 60)

    # 비동기 실행
    result = asyncio.run(test_slack_notification())

    print("\n" + "=" * 60)
    if result:
        print("✅ 테스트 성공!")
    else:
        print("❌ 테스트 실패")
    print("=" * 60)

    sys.exit(0 if result else 1)
