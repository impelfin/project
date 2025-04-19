# main.py

import os
import sys
sys.stderr.write(f"[DEBUG] sys.path = {sys.path}\n")
sys.stderr.write(f"[DEBUG] current dir = {os.getcwd()}\n")

# MCP 서버 엔트리
from fastmcp import FastMCP, Context
from PIL import Image as PILImage
import io
import os
import re
import asyncio
import aiohttp
from typing import Tuple
from openai import AsyncOpenAI

# OpenAI 클라이언트 생성
client = AsyncOpenAI()

# MCP 인스턴스 생성 (1시간 타임아웃)
mcp = FastMCP("FastMCP Example", dependencies=["pandas", "numpy"], timeout=3600)

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

# -- SERVER SIDE --
# Create a server that requests LLM completions from the client

@mcp.tool()
async def generate_poem(topic: str, context: Context) -> str:
    """Generate a short poem about the given topic."""
    # Use OpenAI API directly
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a talented poet who writes concise, evocative verses."},
            {"role": "user", "content": f"Write a short poem about {topic}"}
        ],
        timeout=120
    )
    return response.choices[0].message.content

def count_tokens(text: str) -> int:
    """Roughly estimate the number of tokens in a text.
    This is a very rough estimate - actual token count may be higher."""
    # Count CJK characters (each is roughly 2 tokens)
    cjk = len(re.findall(r'[\u4e00-\u9fff]', text)) * 2
    # Count Latin words (each word is roughly 1.3 tokens)
    words = len(re.findall(r'[a-zA-Z]+', text))
    # Count numbers and punctuation (1 token each)
    others = len(re.findall(r'[^a-zA-Z\u4e00-\u9fff\s]', text))
    # Count newlines (1 token each)
    newlines = text.count('\n')
    return cjk + int(words * 1.3) + others + newlines

def split_into_chunks(text: str, max_tokens: int = 300) -> list[str]:
    """Split text into chunks that are small enough for the GPT model to process."""
    # Split into sentences first
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        # Estimate tokens in this sentence
        sentence_tokens = count_tokens(sentence)
        
        # If this sentence alone is too big, split it further
        if sentence_tokens > max_tokens:
            words = sentence.split()
            temp_chunk = []
            temp_size = 0
            for word in words:
                word_tokens = count_tokens(word)
                if temp_size + word_tokens > max_tokens and temp_chunk:
                    chunks.append(' '.join(temp_chunk))
                    temp_chunk = [word]
                    temp_size = word_tokens
                else:
                    temp_chunk.append(word)
                    temp_size += word_tokens
            if temp_chunk:
                chunks.append(' '.join(temp_chunk))
            continue
        
        # If adding this sentence would exceed limit
        if current_size + sentence_tokens > max_tokens and current_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_size = sentence_tokens
        else:
            current_chunk.append(sentence)
            current_size += sentence_tokens
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

@mcp.tool()
async def start_summarize(document: str, context: Context) -> str:
    """Summarize a document and return the summary.
    
    Args:
        document: The document to summarize. 
        context: The request context
    
    Returns:
        The summarized text or error message
    """
    try:
        # First try as a web URL if it looks like one
        if re.match(r'^https?://', document):
            headers = {'User-Agent': 'Mozilla/5.0'}
            async with aiohttp.ClientSession(headers=headers, timeout=aiohttp.ClientTimeout(total=600)) as session:
                async with session.get(document) as response:
                    if response.status != 200:
                        return f"Error: HTTP {response.status}"
                    content = await response.text()
        # Then try as a file path if it exists
        elif os.path.exists(document):
            with open(document, 'r') as f:
                content = f.read()
        # Finally treat it as direct content
        else:
            content = document

        if not content.strip():
            return "Error: Empty document content"
        
        # Split content into chunks
        chunks = split_into_chunks(content)
        
        # Create tasks for each chunk
        async def process_chunk(chunk):
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Summarize text in 2-3 sentences."}, 
                    {"role": "user", "content": chunk}
                ],
                temperature=0.3,
                max_tokens=100,
                timeout=300
            )
            return response.choices[0].message.content

        # Process chunks in parallel with semaphore
        sem = asyncio.Semaphore(3)  # Max 3 concurrent API calls
        async def process_with_semaphore(chunk):
            async with sem:
                return await process_chunk(chunk)

        # Create and gather tasks
        tasks = [process_with_semaphore(chunk) for chunk in chunks]
        chunk_summaries = await asyncio.gather(*tasks, return_exceptions=True)

        # Check for errors
        errors = [str(e) for e in chunk_summaries if isinstance(e, Exception)]
        if errors:
            return f"Error processing chunks: {'; '.join(errors)}"

        # Combine summaries if needed
        if len(chunk_summaries) > 1:
            final_response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Combine summaries in 3-4 sentences."}, 
                    {"role": "user", "content": '\n'.join(chunk_summaries)}
                ],
                temperature=0.3,
                max_tokens=150,
                timeout=300
            )
            return final_response.choices[0].message.content
        else:
            return chunk_summaries[0]
    except Exception as e:
        return f"Error: {str(e)}"


# Ensure that the mcp instance is referenced to prevent issues with code execution.
mcp

sys.stderr.write("[DEBUG] mcp object is referenced and ready.\n")