#!/usr/bin/env python3
"""
Claude Desktop용 MCP stdio 진입점

업데이트된 기능:
- team.greeting() - 팀장 인사말
- 자유로운 연락처 형식 (이메일, 전화번호, 오픈카톡 등)
- AI 구독 정보 선택 입력
- 역할 제한 제거 (자유 지원)
"""
import sys
import os
from pathlib import Path

# 환경 변수 설정
# 실제 비밀값 기본 주입 제거 (환경 변수에서만 읽도록)
os.environ.setdefault('MCP_API_KEY', 'demo-key-not-secret')
os.environ.setdefault('SLACK_WEBHOOK_URL', '')

# 경로 설정
sys.path.insert(0, str(Path(__file__).parent))

# MCP 서버 임포트 및 실행
from server import mcp

if __name__ == "__main__":
    # stdio transport로 실행
    mcp.run(transport="stdio")
