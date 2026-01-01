"""
rag query tools for MCP Server.
"""

import logging
from typing import Optional
import os
import jwt
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp import FastMCP, Context

logging.basicConfig(level=logging.INFO)

JWKS_URI = os.getenv("JWKS_URI")
ISSUER = os.getenv("ISSUER")
AUDIENCE = os.getenv("AUDIENCE")

verifier = JWTVerifier(jwks_uri=JWKS_URI, issuer=ISSUER, audience=AUDIENCE)

mcp = FastMCP(name="MCP Web Server", auth=verifier)


def get_user_info(jwt_token: str):
    """
    Decodes JWT and returns the preferred_username from the payload.
    """
    token = jwt_token.removeprefix("Bearer ").strip()
    payload = jwt.decode(token, options={"verify_signature": False})
    return payload.get("preferred_username")


@mcp.tool
def maplestory(
    chatInput: str,
    sessionId: Optional[str] = None,
    action: Optional[str] = None,
    toolCallId: Optional[str] = None,
    ctx: Context = None,
) -> str:
    """
    與楓之谷相關的RAG資料庫查詢
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
    # response = client.search(query=chatInput)
    return "最近開放水世界"

app = mcp.http_app()
