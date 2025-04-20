# main.py

import os
import sys
sys.stderr.write(f"[DEBUG] sys.path = {sys.path}\n")
sys.stderr.write(f"[DEBUG] current dir = {os.getcwd()}\n")

# MCP 서버 엔트리
from fastmcp import FastMCP, Context
from PIL import Image as PILImage
import io
from openai import AsyncOpenAI

# secret.json에서 OPENAI_API_KEY 읽기
import json
import os

SECRET_PATH = os.path.join(os.path.dirname(__file__), 'secret.json')
try:
    with open(SECRET_PATH, 'r') as f:
        secret = json.load(f)
    OPENAI_API_KEY = secret.get('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise RuntimeError('OPENAI_API_KEY가 secret.json에 없습니다.')
except FileNotFoundError:
    raise RuntimeError('secret.json 파일을 찾을 수 없습니다.')
except json.JSONDecodeError:
    raise RuntimeError('secret.json 파일이 잘못된 형식입니다.')

# OpenAI 클라이언트 생성
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# MCP 인스턴스 생성
mcp = FastMCP("FastMCP Example", dependencies=["pandas", "numpy"])

sys.stderr.write("[DEBUG] FastMCP instance created.\n")

# 외부 라이브러리
import httpx
from pydantic import BaseModel

# 메시지 정의 (base.py에서 import)
from prompts.base import Message, UserMessage, AssistantMessage


# -------------------------------
# Pydantic 모델 정의
# -------------------------------
class ImageData(BaseModel):
    data: bytes
    format: str = 'png'

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


# -------------------------------
# Context Resources & Tools
# -------------------------------
@mcp.resource("system://status/{system_id}")
async def get_system_status(system_id: str) -> dict:
    """Checks system status and logs information."""
    # Perform checks
    return {"status": "OK", "load": 0.5, "system": system_id}

@mcp.tool()
async def process_large_file(file_uri: str, ctx: Context) -> str:
    """Processes a large file, reporting progress and reading resources."""
    await ctx.info(f"Starting processing for {file_uri}")
    # Read the resource using the context
    file_content_resource = await ctx.read_resource(file_uri)
    file_content = file_content_resource[0].content  # Assuming single text content
    lines = file_content.splitlines()
    total_lines = len(lines)

    for i, line in enumerate(lines):
        # Process line...
        if (i + 1) % 100 == 0:  # Report progress every 100 lines
            await ctx.report_progress(i + 1, total_lines)

    await ctx.info(f"Finished processing {file_uri}")
    return f"Processed {total_lines} lines."


# -------------------------------
# Image Tools
# -------------------------------

@mcp.tool()
def create_thumbnail(image_data: ImageData) -> ImageData:
    """Creates a 100x100 thumbnail from the provided image."""
    img = PILImage.open(io.BytesIO(image_data.data))
    img.thumbnail((100, 100))
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    # Return a new ImageData object with the thumbnail data
    return ImageData(data=buffer.getvalue(), format="png")

@mcp.tool()
def load_image_from_disk(path: str) -> ImageData:
    """Loads an image from the specified path."""
    with open(path, 'rb') as f:
        data = f.read()
    # Get format from file extension
    format = path.split('.')[-1].lower()
    return ImageData(data=data, format=format)

# -------------------------------
# LLM Sampling
# -------------------------------

@mcp.tool()
async def generate_poem(topic: str, context: Context) -> str:
    """Generate a short poem about the given topic."""
    # Use OpenAI API directly
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a talented poet who writes concise, evocative verses."},
            {"role": "user", "content": f"Write a short poem about {topic}"}
        ]
    )
    return response.choices[0].message.content

@mcp.tool()
async def summarize_document(document: str, context: Context) -> str:
    """Summarize a document using server-side LLM capabilities.
    
    Args:
        document: Either a resource URI (e.g., 'system://docs/example.txt') or the actual document content
        context: The MCP context
    
    Returns:
        A concise summary of the document
    """
    # Check if the input is a resource URI
    if document.startswith(('system://', 'config://', 'db://', 'data://')):        
        try:
            # Try to read it as a resource
            doc_resource = await context.read_resource(document)
            content = doc_resource[0].content  # Assuming single text content
        except Exception as e:
            return f"Error reading resource: {str(e)}"
    else:
        # Treat the input as the actual document content
        content = document
    
    # Use OpenAI API directly
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert summarizer. Create a concise summary."},
            {"role": "user", "content": f"Summarize the following document:\n\n{content}"}
        ]
    )
    return response.choices[0].message.content


# Ensure that the mcp instance is referenced to prevent issues with code execution.
mcp

sys.stderr.write("[DEBUG] mcp object is referenced and ready.\n")
