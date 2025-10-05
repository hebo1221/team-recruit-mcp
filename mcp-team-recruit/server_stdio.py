#!/usr/bin/env python3
"""
MCP 서버 STDIO 모드 (테스트용)
HTTP 서버 대신 stdio로 통신
"""
import sys
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

# server.py의 함수들을 임포트
from server import (
    mcp,
    ping,
    faq,
    apply,
    openings,
    timeline,
    intro_template
)

async def main():
    """STDIO 서버 실행"""
    # FastMCP의 내부 서버 객체 사용
    async with stdio_server() as (read_stream, write_stream):
        await mcp.run(
            read_stream,
            write_stream,
            mcp.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
