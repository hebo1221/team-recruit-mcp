from setuptools import setup, find_packages

setup(
    name="mcp-team-recruit",
    version="1.0.0",
    description="MAICON 2025 팀 빌딩 MCP 서버 (FastMCP HTTP)",
    author="김정훈",
    author_email="your-email@example.com",
    url="https://github.com/yourusername/mcp-team-recruit",
    packages=find_packages(),
    py_modules=["server"],
    install_requires=[
        "mcp>=0.1.0",
        "uvicorn>=0.30.0",
        "starlette>=0.38.0",
        "httpx>=0.27.0",
        "pydantic>=2.7.0",
        "email-validator>=2.1.0",
    ],
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
