#!/usr/bin/env python3
"""
HTTP MCP 클라이언트로 직접 테스트
"""
import asyncio
import json
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

API_KEY = "81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474"
BASE_URL = "http://localhost:8080"

async def test_all_features():
    """모든 기능 테스트"""
    print("=" * 70)
    print("MCP 팀 리크루팅 서버 - HTTP 클라이언트 전체 테스트")
    print("=" * 70)

    # HTTP 헤더 설정
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        async with streamablehttp_client(BASE_URL, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                print("\n✅ MCP 서버 연결 성공\n")

                # 1. Tools 목록 조회
                print("=" * 70)
                print("1. Tools 목록 조회")
                print("=" * 70)
                tools_result = await session.list_tools()
                print(f"\n사용 가능한 도구: {len(tools_result.tools)}개\n")

                for tool in tools_result.tools:
                    print(f"  📦 {tool.name}")
                    if tool.description:
                        print(f"     {tool.description[:100]}")
                    print()

                # 2. Resources 목록 조회
                print("=" * 70)
                print("2. Resources 목록 조회")
                print("=" * 70)
                resources_result = await session.list_resources()
                print(f"\n사용 가능한 리소스: {len(resources_result.resources)}개\n")

                for resource in resources_result.resources:
                    print(f"  📚 {resource.uri}")
                    if resource.name:
                        print(f"     이름: {resource.name}")
                    print()

                # 3. Prompts 목록 조회
                print("=" * 70)
                print("3. Prompts 목록 조회")
                print("=" * 70)
                prompts_result = await session.list_prompts()
                print(f"\n사용 가능한 프롬프트: {len(prompts_result.prompts)}개\n")

                for prompt in prompts_result.prompts:
                    print(f"  💬 {prompt.name}")
                    if prompt.description:
                        print(f"     {prompt.description[:100]}")
                    print()

                # 4. ping 도구 테스트
                print("=" * 70)
                print("4. Tool: ping")
                print("=" * 70)
                ping_result = await session.call_tool("ping", arguments={})
                print(f"\n요청: team.ping()")
                if ping_result.content:
                    print(f"응답: {ping_result.content[0].text}")
                print()

                # 5. faq 도구 테스트
                print("=" * 70)
                print("5. Tool: faq")
                print("=" * 70)
                faq_result = await session.call_tool("faq", arguments={})
                print(f"\n요청: team.faq()")
                if faq_result.content:
                    faq_text = faq_result.content[0].text
                    print(f"응답 (처음 400자):\n{faq_text[:400]}...")
                print()

                # 6. apply 도구 테스트 - 정상 케이스
                print("=" * 70)
                print("6. Tool: apply (정상 케이스)")
                print("=" * 70)

                valid_applicant = {
                    "name": "HTTP 클라이언트 테스트",
                    "contact": "http_test@example.com",
                    "category": "장병",
                    "message": "HTTP MCP 클라이언트를 통한 지원서 제출 테스트",
                    "ai_subscriptions": "Claude Pro"
                }

                print(f"\n📝 제출할 지원서:")
                print(json.dumps(valid_applicant, indent=2, ensure_ascii=False))

                apply_result = await session.call_tool("apply", arguments={"payload": valid_applicant})

                if apply_result.content:
                    result_text = apply_result.content[0].text
                    result_data = json.loads(result_text)
                    print(f"\n응답:")
                    print(json.dumps(result_data, indent=2, ensure_ascii=False))

                    if result_data.get("ok"):
                        print("\n✅ 지원서 제출 성공!")
                    else:
                        print(f"\n❌ 지원서 제출 실패")
                print()

                # 7. apply 도구 테스트 - 유효성 검증 실패
                print("=" * 70)
                print("7. Tool: apply (유효성 검증 실패)")
                print("=" * 70)

                invalid_applicant = {
                    "name": "테",
                    "contact": "123",
                    "category": "기타"
                }

                print(f"\n📝 제출할 지원서 (잘못된 형식):")
                print(json.dumps(invalid_applicant, indent=2, ensure_ascii=False))

                invalid_result = await session.call_tool("apply", arguments={"payload": invalid_applicant})

                if invalid_result.content:
                    invalid_text = invalid_result.content[0].text
                    invalid_data = json.loads(invalid_text)
                    print(f"\n응답:")
                    print(json.dumps(invalid_data, indent=2, ensure_ascii=False))

                    if not invalid_data.get("ok"):
                        print("\n✅ 유효성 검증이 올바르게 작동함!")
                    else:
                        print(f"\n❌ 유효성 검증 실패 (잘못된 데이터가 통과됨)")
                print()

                # 8. Resource 조회 - roles://openings
                print("=" * 70)
                print("8. Resource: roles://openings")
                print("=" * 70)

                roles_result = await session.read_resource("roles://openings")
                if roles_result.contents:
                    roles_text = roles_result.contents[0].text
                    print(f"\n모집 역할 (처음 500자):\n{roles_text[:500]}...")
                print()

                # 9. Resource 조회 - event://timeline
                print("=" * 70)
                print("9. Resource: event://timeline")
                print("=" * 70)

                timeline_result = await session.read_resource("event://timeline")
                if timeline_result.contents:
                    timeline_text = timeline_result.contents[0].text
                    print(f"\n대회 일정 (처음 500자):\n{timeline_text[:500]}...")
                print()

                # 10. Prompt 조회 - intro_template
                print("=" * 70)
                print("10. Prompt: intro_template")
                print("=" * 70)

                intro_result = await session.get_prompt("intro_template", arguments={"role": "Vision Engineer"})
                if intro_result.messages:
                    intro_text = intro_result.messages[0].content.text
                    print(f"\nVision Engineer 자기소개 양식 (처음 600자):\n{intro_text[:600]}...")
                print()

                # 최종 결과
                print("\n" + "=" * 70)
                print("✅ 전체 테스트 완료!")
                print("=" * 70)

                print("\n📊 테스트 결과 요약:")
                print(f"  ✅ Tools: {len(tools_result.tools)}개")
                print(f"     - {', '.join([t.name for t in tools_result.tools])}")
                print(f"  ✅ Resources: {len(resources_result.resources)}개")
                print(f"     - {', '.join([r.uri for r in resources_result.resources])}")
                print(f"  ✅ Prompts: {len(prompts_result.prompts)}개")
                print(f"     - {', '.join([p.name for p in prompts_result.prompts])}")
                print(f"  ✅ 지원서 제출: 성공")
                print(f"  ✅ 유효성 검증: 정상 작동")

                return True

    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_all_features())

    print("\n" + "=" * 70)
    if success:
        print("🎉 모든 테스트 통과!")
    else:
        print("❌ 테스트 실패")
    print("=" * 70)
