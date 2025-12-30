from fastmcp import FastMCP
import logging
from typing import Optional
from tavily import TavilyClient
import os

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
logging.basicConfig(level=logging.INFO)

mcp = FastMCP(name="MCP Web Server")
client = TavilyClient(api_key=TAVILY_API_KEY)

@mcp.tool
def web_search(
    chatInput: str,
    sessionId: Optional[str] = None,
    action: Optional[str] = None,
    toolCallId: Optional[str] = None,
) -> str:
    """
    Perform a real-time web search and return a gentle, easy-to-read summary
    of the latest information.

    Parameters:
    - chatInput (required): The user’s search query or question. This value
      must be provided, as it is the text that will be used for the search.
    - sessionId (optional): Conversation session identifier.
    - action (optional): Optional action identifier.
    - toolCallId (optional): Tool invocation identifier.

    Returns:
    - A plain-text summary that combines relevant search result content.

    Notes:
    - This tool is helpful when up-to-date or real-world information is needed.
    - If no chatInput is provided, no meaningful search results can be returned.
    - The content is gathered from multiple sources and combined into one
      continuous response for convenience.
    """
    logging.info(
        f"chatInput={chatInput}, sessionId={sessionId}, action={action}, toolCallId={toolCallId}"
    )
    response = client.search(query=chatInput)
    return "".join(search["content"] for search in response["results"])


app = mcp.http_app()
