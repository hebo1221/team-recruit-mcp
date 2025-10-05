#!/usr/bin/env python3
"""
구분 필드 테스트 (장병/사관생도/일반인)
"""
import sys
import os
import asyncio

os.environ['SLACK_WEBHOOK_URL'] = 'https://example.com/slack-webhook'
os.environ['MCP_API_KEY'] = '81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474'

sys.path.insert(0, os.path.dirname(__file__))

from server import Applicant, save_applicant, send_slack_notification

async def test_category_field():
    """구분 필드 테스트"""
    print("\n" + "=" * 70)
    print("구분 필드 테스트 (장병/사관생도/일반인)")
    print("=" * 70)

    # 장병
    soldier = Applicant(
        name="이병 김철수",
        contact="soldier@example.com",
        category="장병",
        message="복무 중 AI 기술을 배우고 싶습니다.",
        ai_subscriptions="ChatGPT Plus"
    )

    print("\n1️⃣  장병:")
    print(f"   이름: {soldier.name}")
    print(f"   구분: {soldier.category}")

    save1 = save_applicant(soldier)
    slack1 = await send_slack_notification(soldier)
    print(f"   {'✅' if save1 and slack1 else '❌'} 제출 성공")

    # 사관생도
    cadet = Applicant(
        name="사관생도 박영희",
        contact="010-5678-1234",
        category="사관생도"
    )

    print("\n2️⃣  사관생도:")
    print(f"   이름: {cadet.name}")
    print(f"   구분: {cadet.category}")

    save2 = save_applicant(cadet)
    slack2 = await send_slack_notification(cadet)
    print(f"   {'✅' if save2 and slack2 else '❌'} 제출 성공")

    # 일반인
    civilian = Applicant(
        name="일반인 최민수",
        contact="civilian@example.com",
        category="일반인",
        message="대학원생입니다.",
        ai_subscriptions="Claude Pro"
    )

    print("\n3️⃣  일반인:")
    print(f"   이름: {civilian.name}")
    print(f"   구분: {civilian.category}")

    save3 = save_applicant(civilian)
    slack3 = await send_slack_notification(civilian)
    print(f"   {'✅' if save3 and slack3 else '❌'} 제출 성공")

    print("\n" + "=" * 70)
    print("🎉 구분 필드 테스트 완료!")
    print("\n필수 필드:")
    print("   - name ✅")
    print("   - contact ✅")
    print("   - category ✅ (장병/사관생도/일반인)")
    print("=" * 70 + "\n")

    return all([save1, slack1, save2, slack2, save3, slack3])

if __name__ == "__main__":
    result = asyncio.run(test_category_field())
    sys.exit(0 if result else 1)
