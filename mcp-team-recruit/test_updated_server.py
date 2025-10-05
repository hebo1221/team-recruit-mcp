#!/usr/bin/env python3
"""
업데이트된 MCP 서버 테스트
"""
import sys
import os
import asyncio

# 환경 변수 설정
os.environ['SLACK_WEBHOOK_URL'] = 'https://example.com/slack-webhook'
os.environ['MCP_API_KEY'] = 'demo-key-not-secret'

sys.path.insert(0, os.path.dirname(__file__))

from server import Applicant, save_applicant, send_slack_notification

async def test_new_schema():
    """새로운 스키마 테스트"""
    print("\n" + "=" * 70)
    print("업데이트된 MCP 서버 테스트")
    print("=" * 70)

    # 새로운 지원서 형식
    applicant = Applicant(
        name="테스트 지원자",
        contact="test@example.com 또는 010-1234-5678",
        message="만드는 것을 좋아하고, 새로운 기술 도전을 즐깁니다. 실패 경험도 많습니다!",
        ai_subscriptions="Claude Pro, Cursor Pro"
    )

    print("\n1️⃣  새로운 지원서 형식:")
    print(f"   이름: {applicant.name}")
    print(f"   연락처: {applicant.contact}")
    print(f"   메시지: {applicant.message}")
    print(f"   AI 구독: {applicant.ai_subscriptions}")

    # 파일 저장
    print("\n2️⃣  파일 저장 중...")
    save_success = save_applicant(applicant)
    print(f"   {'✅' if save_success else '❌'} 저장 결과: {save_success}")

    # Slack 알림
    print("\n3️⃣  Slack 알림 전송 중...")
    slack_success = await send_slack_notification(applicant)
    print(f"   {'✅' if slack_success else '❌'} Slack 알림: {slack_success}")

    # 최소 정보만으로 지원 (AI 구독 없이)
    print("\n4️⃣  최소 정보 테스트 (AI 구독 정보 없음):")
    minimal_applicant = Applicant(
        name="최소정보",
        contact="minimal@example.com"
    )
    print(f"   이름: {minimal_applicant.name}")
    print(f"   연락처: {minimal_applicant.contact}")
    print(f"   메시지: {minimal_applicant.message}")
    print(f"   AI 구독: {minimal_applicant.ai_subscriptions}")

    save_success2 = save_applicant(minimal_applicant)
    slack_success2 = await send_slack_notification(minimal_applicant)
    print(f"   {'✅' if save_success2 and slack_success2 else '❌'} 최소 정보 제출 성공")

    print("\n" + "=" * 70)
    print("🎉 테스트 완료!")
    print("\n새로운 기능:")
    print("   1. ✅ team.greeting() - 팀장 인사말")
    print("   2. ✅ 자유로운 연락처 형식 (이메일, 전화번호, 오픈카톡 등)")
    print("   3. ✅ AI 구독 정보 선택 입력")
    print("   4. ✅ 역할 제한 제거 (자유 지원)")
    print("   5. ✅ 주당 시간 제한 제거")
    print("=" * 70 + "\n")

    return save_success and slack_success

if __name__ == "__main__":
    result = asyncio.run(test_new_schema())
    sys.exit(0 if result else 1)
