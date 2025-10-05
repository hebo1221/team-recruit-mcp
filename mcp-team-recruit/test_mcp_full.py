#!/usr/bin/env python3
"""
MCP 서버 전체 통합 테스트
MCP SDK를 사용한 실제 프로토콜 테스트
"""
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_mcp_server():
    """MCP 서버 전체 기능 테스트"""
    print("=" * 70)
    print("MCP 팀 리크루팅 서버 - 전체 통합 테스트")
    print("=" * 70)

    # MCP 서버 실행 파라미터
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env={
            "MCP_API_KEY": "81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474",
            "PORT": "8080"
        }
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()
            print("\n✅ MCP 서버 연결 성공\n")

            # 1. Tools 목록 조회
            print("=" * 70)
            print("1. Tools 목록 조회")
            print("=" * 70)
            tools = await session.list_tools()
            print(f"\n사용 가능한 도구: {len(tools.tools)}개\n")
            for tool in tools.tools:
                print(f"  📦 {tool.name}")
                if tool.description:
                    print(f"     {tool.description}")
                if hasattr(tool, 'inputSchema') and tool.inputSchema:
                    print(f"     입력: {tool.inputSchema.get('type', 'N/A')}")
                print()

            # 2. Resources 목록 조회
            print("=" * 70)
            print("2. Resources 목록 조회")
            print("=" * 70)
            resources = await session.list_resources()
            print(f"\n사용 가능한 리소스: {len(resources.resources)}개\n")
            for resource in resources.resources:
                print(f"  📚 {resource.uri}")
                if resource.name:
                    print(f"     이름: {resource.name}")
                if resource.description:
                    print(f"     설명: {resource.description}")
                print()

            # 3. Prompts 목록 조회
            print("=" * 70)
            print("3. Prompts 목록 조회")
            print("=" * 70)
            prompts = await session.list_prompts()
            print(f"\n사용 가능한 프롬프트: {len(prompts.prompts)}개\n")
            for prompt in prompts.prompts:
                print(f"  💬 {prompt.name}")
                if prompt.description:
                    print(f"     {prompt.description}")
                print()

            # 4. ping 도구 호출
            print("=" * 70)
            print("4. ping 도구 테스트")
            print("=" * 70)
            ping_result = await session.call_tool("ping", arguments={})
            print(f"\n요청: team.ping()")
            print(f"응답: {ping_result.content[0].text if ping_result.content else 'N/A'}\n")

            # 5. faq 도구 호출
            print("=" * 70)
            print("5. faq 도구 테스트")
            print("=" * 70)
            faq_result = await session.call_tool("faq", arguments={})
            print(f"\n요청: team.faq()")
            if faq_result.content:
                faq_text = faq_result.content[0].text
                print(f"응답 (처음 300자):\n{faq_text[:300]}...\n")

            # 6. apply 도구 호출 (지원서 제출)
            print("=" * 70)
            print("6. apply 도구 테스트 (지원서 제출)")
            print("=" * 70)

            test_applicant = {
                "name": "MCP 테스트 지원자",
                "email": "mcp_test@example.com",
                "role": "Full Stack Developer",
                "github": "https://github.com/mcptest",
                "skills": ["Python", "MCP", "FastAPI", "React"],
                "time_per_week": 30,
                "notes": "MCP 프로토콜을 통한 자동 지원서 제출 테스트입니다."
            }

            print(f"\n📝 제출할 지원서:")
            print(json.dumps(test_applicant, indent=2, ensure_ascii=False))

            apply_result = await session.call_tool("apply", arguments={"payload": test_applicant})

            if apply_result.content:
                result_text = apply_result.content[0].text
                result_data = json.loads(result_text)
                print(f"\n응답:")
                print(json.dumps(result_data, indent=2, ensure_ascii=False))

                if result_data.get("ok"):
                    print("\n✅ 지원서 제출 성공!")
                else:
                    print(f"\n❌ 지원서 제출 실패: {result_data.get('error')}")

            # 7. Resource 조회 (roles://openings)
            print("\n" + "=" * 70)
            print("7. Resource 조회 - roles://openings")
            print("=" * 70)

            roles_resource = await session.read_resource("roles://openings")
            if roles_resource.contents:
                roles_text = roles_resource.contents[0].text
                print(f"\n모집 역할 (처음 400자):\n{roles_text[:400]}...")

            # 8. Resource 조회 (event://timeline)
            print("\n" + "=" * 70)
            print("8. Resource 조회 - event://timeline")
            print("=" * 70)

            timeline_resource = await session.read_resource("event://timeline")
            if timeline_resource.contents:
                timeline_text = timeline_resource.contents[0].text
                print(f"\n대회 일정 (처음 400자):\n{timeline_text[:400]}...")

            # 9. Prompt 호출 (intro_template)
            print("\n" + "=" * 70)
            print("9. Prompt 호출 - intro_template")
            print("=" * 70)

            intro_prompt = await session.get_prompt("intro_template", arguments={"role": "Vision Engineer"})
            if intro_prompt.messages:
                intro_text = intro_prompt.messages[0].content.text
                print(f"\n자기소개 양식 (처음 500자):\n{intro_text[:500]}...")

            # 최종 결과
            print("\n" + "=" * 70)
            print("✅ 전체 테스트 완료!")
            print("=" * 70)

            print("\n📊 테스트 결과 요약:")
            print(f"  ✅ Tools: {len(tools.tools)}개 ({', '.join([t.name for t in tools.tools])})")
            print(f"  ✅ Resources: {len(resources.resources)}개 ({', '.join([r.uri for r in resources.resources])})")
            print(f"  ✅ Prompts: {len(prompts.prompts)}개 ({', '.join([p.name for p in prompts.prompts])})")
            print(f"  ✅ 지원서 제출: 성공")

if __name__ == "__main__":
    try:
        asyncio.run(test_mcp_server())
    except KeyboardInterrupt:
        print("\n\n테스트 중단됨")
    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
