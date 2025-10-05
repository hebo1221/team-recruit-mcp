#!/usr/bin/env python3
"""
MCP HTTP-to-STDIO Wrapper
HTTP MCP 서버를 stdio transport로 변환하는 wrapper
"""
import sys
import json
import httpx
import asyncio
from typing import Any

# HTTP MCP 서버 URL
MCP_SERVER_URL = "https://maicon2025-team-recruit-278861544731.asia-northeast3.run.app/mcp"

class MCPHTTPClient:
    """HTTP MCP 서버와 통신하는 stdio wrapper"""

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session_id = None

    async def send_request(self, request: dict) -> dict:
        """HTTP MCP 서버로 요청 전송"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.server_url,
                json=request,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream"
                }
            )

            # SSE 응답 파싱
            content = response.text

            # SSE 형식 확인
            if "event: message" in content and "data: " in content:
                # SSE 형식에서 JSON 추출
                lines = content.split("\n")
                for line in lines:
                    if line.startswith("data: "):
                        json_str = line[6:]  # "data: " 제거
                        return json.loads(json_str)

            # 일반 JSON 응답
            if content.strip():
                return json.loads(content)

            # 빈 응답
            raise ValueError("Empty response from server")

    async def handle_stdio(self):
        """stdin에서 JSON-RPC 요청을 읽고 HTTP로 전달 후 stdout으로 응답"""
        while True:
            try:
                # stdin에서 한 줄씩 읽기
                line = sys.stdin.readline()
                if not line:
                    break

                line = line.strip()
                if not line:
                    continue

                # JSON-RPC 요청 파싱
                request = json.loads(line)

                # HTTP MCP 서버로 전달
                response = await self.send_request(request)

                # stdout으로 응답 출력
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                sys.stdout.write(json.dumps(error_response) + "\n")
                sys.stdout.flush()

async def async_main():
    """비동기 메인 함수"""
    client = MCPHTTPClient(MCP_SERVER_URL)
    await client.handle_stdio()

def main():
    """Entry point for console script"""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
