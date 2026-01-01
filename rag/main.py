"""
rag query tools for MCP Server.
"""

import logging
from typing import Optional
import os
import jwt
import httpx
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp import FastMCP, Context

logging.basicConfig(level=logging.INFO)

JWKS_URI = os.getenv("JWKS_URI")
ISSUER = os.getenv("ISSUER")
AUDIENCE = os.getenv("AUDIENCE")

verifier = JWTVerifier(jwks_uri=JWKS_URI, issuer=ISSUER, audience=AUDIENCE)
mcp = FastMCP(name="MCP Web Server", auth=verifier)

URL = "http://mcp-rag-service:8000/query"

def get_user_info(jwt_token: str):
    """
    Decodes JWT and returns the preferred_username from the payload.
    """
    token = jwt_token.removeprefix("Bearer ").strip()
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload.get("preferred_username")


@mcp.tool
async def maplestory(
    chatInput: str,
    sessionId: Optional[str] = None,
    action: Optional[str] = None,
    toolCallId: Optional[str] = None,
    ctx: Context = None,
) -> str:
    """
    Search the MapleStory RAG database for game-related information. 
    Use this tool to retrieve details about game mechanics, items, quests, 
    bosses, or recent updates for MapleStory.
    
    Args:
        chatInput: The specific question or search query about MapleStory.
    """
    token = ctx.request_context.request.headers.get("Authorization")
    service_account = get_user_info(token)
    logging.info(
        "user=%s, chatInput=%s, sessionId=%s, action=%s, toolCallId=%s",
        service_account,
        chatInput,
        sessionId,
        action,
        toolCallId,
    )
    payload = {
        "request": {
            "prompt": chatInput
        },
        "query_name": "maplestory"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    if token:
        headers["Authorization"] = token
    # 3. Execute the Async HTTP POST request
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(URL, json=payload, headers=headers)
            # Raise an exception for 4xx or 5xx status codes
            response.raise_for_status()
            return response.text

    except httpx.HTTPStatusError as e:
        logging.error("RAG Service HTTP error: %s - %s", e.response.status_code, e.response.text)
        return f"Retrieval service error (Status: {e.response.status_code})"
    except httpx.RequestError as e:
        logging.error("Network error while reaching RAG service: %s", e)
        return "The RAG service is currently unreachable."

app = mcp.http_app()
