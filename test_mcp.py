#!/usr/bin/env python3
"""
MCP 서버 테스트 스크립트
"""
import httpx
import json
import os

# 설정
BASE_URL = "http://localhost:8080"
API_KEY = os.getenv("MCP_API_KEY", "81e3309185b4ea4f64c36b079542c1be1b5a4a7fb9d29474")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_ping():
    """ping 도구 테스트"""
    print("\n=== ping 도구 테스트 ===")

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "ping",
            "arguments": {}
        }
    }

    response = httpx.post(BASE_URL, headers=headers, json=payload, timeout=10)
    print(f"상태 코드: {response.status_code}")
    print(f"응답: {response.text}")
    return response.json()

def test_faq():
    """faq 도구 테스트"""
    print("\n=== faq 도구 테스트 ===")

    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "faq",
            "arguments": {}
        }
    }

    response = httpx.post(BASE_URL, headers=headers, json=payload, timeout=10)
    print(f"상태 코드: {response.status_code}")
    result = response.json()
    if "result" in result and "content" in result["result"]:
        for item in result["result"]["content"]:
            if item["type"] == "text":
                print(f"FAQ:\n{item['text'][:200]}...")
    return result

def test_apply():
    """apply 도구 테스트 (지원서 제출)"""
    print("\n=== apply 도구 테스트 ===")

    applicant_data = {
        "name": "테스트 지원자",
        "email": "test@example.com",
        "role": "Vision Engineer",
        "github": "https://github.com/testuser",
        "skills": ["YOLO", "PyTorch", "DeepStream"],
        "time_per_week": 20,
        "notes": "로컬 테스트용 지원서입니다."
    }

    payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "apply",
            "arguments": {
                "payload": applicant_data
            }
        }
    }

    response = httpx.post(BASE_URL, headers=headers, json=payload, timeout=10)
    print(f"상태 코드: {response.status_code}")
    result = response.json()
    print(f"응답: {json.dumps(result, indent=2, ensure_ascii=False)}")
    return result

def test_list_tools():
    """사용 가능한 도구 목록 조회"""
    print("\n=== 도구 목록 조회 ===")

    payload = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/list"
    }

    response = httpx.post(BASE_URL, headers=headers, json=payload, timeout=10)
    print(f"상태 코드: {response.status_code}")
    result = response.json()
    if "result" in result and "tools" in result["result"]:
        print(f"사용 가능한 도구: {len(result['result']['tools'])}개")
        for tool in result["result"]["tools"]:
            print(f"  - {tool['name']}: {tool.get('description', 'N/A')}")
    return result

def test_list_resources():
    """사용 가능한 리소스 목록 조회"""
    print("\n=== 리소스 목록 조회 ===")

    payload = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "resources/list"
    }

    response = httpx.post(BASE_URL, headers=headers, json=payload, timeout=10)
    print(f"상태 코드: {response.status_code}")
    result = response.json()
    if "result" in result and "resources" in result["result"]:
        print(f"사용 가능한 리소스: {len(result['result']['resources'])}개")
        for resource in result["result"]["resources"]:
            print(f"  - {resource['uri']}: {resource.get('name', 'N/A')}")
    return result

if __name__ == "__main__":
    try:
        # 헬스체크
        print("=== 헬스체크 ===")
        health_response = httpx.get(f"{BASE_URL}/healthz", timeout=5)
        print(f"헬스체크: {health_response.text}")

        # MCP 테스트
        test_list_tools()
        test_list_resources()
        test_ping()
        test_faq()
        test_apply()

        print("\n✅ 모든 테스트 완료!")

    except Exception as e:
        print(f"\n❌ 테스트 실패: {e}")
        import traceback
        traceback.print_exc()
