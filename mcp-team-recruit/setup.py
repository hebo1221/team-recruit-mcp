from setuptools import setup, find_packages

setup(
    name="mcp-team-recruit",
    version="1.0.0",
    description="MAICON 2025 팀 빌딩 MCP 서버 - HTTP wrapper for Claude Desktop",
    author="김정훈",
    author_email="your-email@example.com",
    url="https://github.com/yourusername/mcp-team-recruit",
    py_modules=["mcp_client"],
    install_requires=[
        "httpx>=0.24.0",
    ],
    entry_points={
        "console_scripts": [
            "mcp-team-recruit=mcp_client:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
