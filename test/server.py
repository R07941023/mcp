from fastmcp import FastMCP
import logging
from typing import Optional
from tavily import TavilyClient

logging.basicConfig(level=logging.DEBUG)

mcp = FastMCP(name="My Remote MCP Server")

@mcp.tool
def get_weather(
    country: Optional[str] = None,
    chatInput: Optional[str] = None,
    sessionId: Optional[str] = None,
    action: Optional[str] = None,
    toolCallId: Optional[str] = None
) -> str:
    """
    支援 n8n AI Agent 的 get_weather 工具
    """
    logging.info(f"country={country}, chatInput={chatInput}, sessionId={sessionId}, action={action}, toolCallId={toolCallId}")

    # 使用 country 或 fallback chatInput
    location = country or chatInput or "未知地點"
    return f"{location} 的天氣是：多雪 ❄️"

@mcp.tool
def web_search(
    country: Optional[str] = None,
    chatInput: Optional[str] = None,
    sessionId: Optional[str] = None,
    action: Optional[str] = None,
    toolCallId: Optional[str] = None
) -> str:
    """
    支援即時線上搜索資訊
    """
    logging.info(f"country={country}, chatInput={chatInput}, sessionId={sessionId}, action={action}, toolCallId={toolCallId}")

    client = TavilyClient("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")
    response = client.search(
        query="今天高雄的天氣如何?"
    )
    res = ''
    for search in response['results']:
        res += search['content']
    return res


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8080,
        path="/mcp"
    )