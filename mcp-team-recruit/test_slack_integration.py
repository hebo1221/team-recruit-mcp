#!/usr/bin/env python3
"""
Slack 웹훅 통합 테스트 (server.py 함수 직접 사용)
"""
import sys
import os
import asyncio

# 환경 변수 먼저 로드
os.environ['SLACK_WEBHOOK_URL'] = 'https://example.com/slack-webhook'
os.environ['MCP_API_KEY'] = 'demo-key-not-secret'

sys.path.insert(0, os.path.dirname(__file__))

from server import Applicant, send_slack_notification

async def test_slack():
    """Slack 알림 테스트"""
    print("\n" + "=" * 70)
    print("Slack 웹훅 통합 테스트")
    print("=" * 70)

    # 테스트 지원자
    test_applicant = Applicant(
        name="김정훈 (Slack 테스트)",
        email="slack_test@example.com",
        role="Vision Engineer",
        github="https://github.com/kjh",
        skills=["YOLO", "DeepStream", "PyTorch", "Jetson"],
        time_per_week=25,
        notes="Slack 알림 통합 테스트입니다. 이 메시지가 보이면 성공!"
    )

    print(f"\n📝 테스트 지원자:")
    print(f"   이름: {test_applicant.name}")
    print(f"   이메일: {test_applicant.email}")
    print(f"   역할: {test_applicant.role}")
    print(f"   스킬: {', '.join(test_applicant.skills)}")

    print("\n📤 Slack 알림 전송 중...")

    # 알림 전송
    success = await send_slack_notification(test_applicant)

    print("\n" + "=" * 70)
    if success:
        print("✅ Slack 알림 전송 성공!")
        print("\n📱 Slack 채널에서 메시지를 확인하세요:")
        print("   - 새로운 팀원 지원 알림")
        print("   - 이름, 이메일, 역할, 스킬 등 정보 표시")
    else:
        print("❌ Slack 알림 전송 실패")
    print("=" * 70 + "\n")

    return success

if __name__ == "__main__":
    result = asyncio.run(test_slack())
    sys.exit(0 if result else 1)
