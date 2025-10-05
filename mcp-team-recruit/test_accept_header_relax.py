#!/usr/bin/env python3
"""HTTP Accept 헤더 완화 테스트 스크립트"""
import sys

from starlette.testclient import TestClient

from server import app


def run_test() -> int:
    """Accept 헤더에 text/event-stream만 있어도 초기화가 되는지 확인"""
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "clientInfo": {"name": "accept-test", "version": "1.0"},
            "protocolVersion": "2024-11-05",
            "capabilities": {},
        },
    }

    with TestClient(app) as client:
        response = client.post("/mcp", headers=headers, json=payload)
        status = response.status_code
        body = response.content

        expose = response.headers.get("access-control-expose-headers")
        allow_origin = response.headers.get("access-control-allow-origin")

        options = client.options("/mcp", headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        })

    if status != 200:
        print("❌ 서버가 Accept 헤더를 허용하지 않았습니다.")
        print(f"   상태 코드: {status}")
        print(f"   응답 본문: {body.decode(errors='ignore')}")
        return 1

    if allow_origin != "*":
        print("❌ CORS allow-origin 헤더가 노출되지 않았습니다.")
        print(f"   access-control-allow-origin: {allow_origin}")
        return 1

    if not expose or "mcp-session-id" not in expose:
        print("❌ access-control-expose-headers에 mcp-session-id가 없습니다.")
        print(f"   access-control-expose-headers: {expose}")
        return 1

    if options.status_code != 204:
        print("❌ OPTIONS 프리플라이트 응답 코드가 204가 아닙니다.")
        print(f"   상태 코드: {options.status_code}")
        print(f"   응답 헤더: {options.headers}")
        return 1

    print("✅ Accept 헤더 완화 성공 (HTTP 200 수신)")
    return 0


if __name__ == "__main__":
    sys.exit(run_test())
