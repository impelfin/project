import os
import sys
sys.stderr.write(f"[DEBUG] sys.path = {sys.path}\n")
sys.stderr.write(f"[DEBUG] current dir = {os.getcwd()}\n")

# MCP 서버 엔트리
from fastmcp import FastMCP

# MCP 인스턴스 생성
mcp = FastMCP("My App", dependencies=["pandas", "numpy"])

sys.stderr.write("[DEBUG] FastMCP instance created.\n")

# 외부 라이브러리
import httpx
from pydantic import BaseModel

# 메시지 정의 (base.py에서 import)
from prompts.base import Message, UserMessage, AssistantMessage

# -------------------------------
# Pydantic 모델 정의
# -------------------------------
class UserInfo(BaseModel):
    user_id: int
    notify: bool = False

# -------------------------------
# Tools
# -------------------------------
@mcp.tool()
async def send_notification(user: UserInfo, message: str) -> dict:
    """Sends a notification to a user if requested."""
    if user.notify:
        sys.stderr.write(f"Notifying user {user.user_id}: {message}\n")
        return {"status": "sent", "user_id": user.user_id}
    return {"status": "skipped", "user_id": user.user_id}

@mcp.tool()
def get_stock_price(ticker: str) -> float:
    """Gets the current price for a stock ticker."""
    prices = {"AAPL": 180.50, "GOOG": 140.20}
    return prices.get(ticker.upper(), 0.0)

# -------------------------------
# Resources
# -------------------------------
@mcp.resource("config://app-version")
def get_app_version() -> str:
    return "v2.1.0"

@mcp.resource("db://users/{user_id}/email")
async def get_user_email(user_id: str) -> str:
    emails = {"123": "alice@example.com", "456": "bob@example.com"}
    return emails.get(user_id, "not_found@example.com")

@mcp.resource("data://product-categories")
def get_categories() -> list[str]:
    return ["Electronics", "Books", "Home Goods"]

# -------------------------------
# Prompts
# -------------------------------
@mcp.prompt()
def ask_review(code_snippet: str) -> str:
    """Generates a standard code review request."""
    return f"Please review the following code snippet for potential bugs and style issues:\n```python\n{code_snippet}\n```"

@mcp.prompt()
def debug_session_start(error_message: str) -> list[Message]:
    """Initiates a debugging help session."""
    return [
        UserMessage(f"I encountered an error:\n{error_message}"),
        AssistantMessage("Okay, I can help with that. Can you provide the full traceback and tell me what you were trying to do?")
    ]

# Ensure that the mcp instance is referenced to prevent issues with code execution.
mcp

sys.stderr.write("[DEBUG] mcp object is referenced and ready.\n")