"""
MCP 팀 리크루팅 서버 - HTTP 버전
FastMCP HTTP/SSE transport 사용
"""
import os
from server import mcp

# HTTP/SSE transport로 실행
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))

    # FastMCP SSE transport 실행 (HTTP 엔드포인트 제공)
    mcp.run(transport="sse", port=port)
