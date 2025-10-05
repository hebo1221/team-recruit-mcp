#!/usr/bin/env python3
"""
군 신분 필드 추가 테스트
"""
import sys
import os
import asyncio

os.environ['SLACK_WEBHOOK_URL'] = 'https://example.com/slack-webhook'
os.environ['MCP_API_KEY'] = '81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474'

sys.path.insert(0, os.path.dirname(__file__))

from server import Applicant, save_applicant, send_slack_notification

async def test_military_status():
    """군 신분 필드 테스트"""
    print("\n" + "=" * 70)
    print("군 신분 필드 추가 테스트")
    print("=" * 70)

    # 군장병 지원자
    soldier = Applicant(
        name="이병 김철수",
        contact="soldier@example.com",
        military_status="군장병",
        message="복무 중 AI 기술을 배우고 싶습니다.",
        ai_subscriptions="ChatGPT Plus"
    )

    print("\n1️⃣  군장병 지원자:")
    print(f"   이름: {soldier.name}")
    print(f"   연락처: {soldier.contact}")
    print(f"   군 신분: {soldier.military_status}")
    print(f"   메시지: {soldier.message}")

    save_success1 = save_applicant(soldier)
    slack_success1 = await send_slack_notification(soldier)
    print(f"   {'✅' if save_success1 and slack_success1 else '❌'} 제출 성공")

    # 사관생도 지원자
    cadet = Applicant(
        name="사관생도 박영희",
        contact="010-5678-1234",
        military_status="사관생도",
        message="군사 AI 시스템에 관심이 많습니다."
    )

    print("\n2️⃣  사관생도 지원자:")
    print(f"   이름: {cadet.name}")
    print(f"   연락처: {cadet.contact}")
    print(f"   군 신분: {cadet.military_status}")
    print(f"   AI 구독: {cadet.ai_subscriptions}")

    save_success2 = save_applicant(cadet)
    slack_success2 = await send_slack_notification(cadet)
    print(f"   {'✅' if save_success2 and slack_success2 else '❌'} 제출 성공")

    # 일반 지원자
    civilian = Applicant(
        name="일반인 최민수",
        contact="civilian@example.com",
        military_status="해당없음",
        message="대학원생입니다. 팀 프로젝트 경험을 쌓고 싶습니다.",
        ai_subscriptions="Claude Pro"
    )

    print("\n3️⃣  일반 지원자:")
    print(f"   이름: {civilian.name}")
    print(f"   연락처: {civilian.contact}")
    print(f"   군 신분: {civilian.military_status}")

    save_success3 = save_applicant(civilian)
    slack_success3 = await send_slack_notification(civilian)
    print(f"   {'✅' if save_success3 and slack_success3 else '❌'} 제출 성공")

    print("\n" + "=" * 70)
    print("🎉 군 신분 필드 테스트 완료!")
    print("\n필수 필드:")
    print("   - name ✅")
    print("   - contact ✅")
    print("   - military_status ✅ (새로 추가)")
    print("\n선택 필드:")
    print("   - message")
    print("   - ai_subscriptions")
    print("=" * 70 + "\n")

    return all([save_success1, slack_success1, save_success2, slack_success2, save_success3, slack_success3])

if __name__ == "__main__":
    result = asyncio.run(test_military_status())
    sys.exit(0 if result else 1)
