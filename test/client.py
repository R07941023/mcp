import asyncio
from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage
from langfuse.langchain import CallbackHandler
from langfuse import Langfuse
import os


os.environ["TAVILY_API_KEY"] = "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"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-b3c57e2f-0927-46bb-b5ab-c2dc30fc10f4"
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-0b7a13c5-657f-439a-9831-314910149763"
os.environ["LANGFUSE_BASE_URL"] = "https://langfuse.mydormroom.dpdns.org"
langfuse = Langfuse()
langfuse_handler = CallbackHandler()

server_url = 'http://host.docker.internal:11434'

async def main():

    # prompt = langfuse.get_prompt("n8n", label="production")
    # print(prompt.get_langchain_prompt())

    # 1. 初始化 MCP Client 並取得工具定義
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "streamable_http",
                "url": "http://host.docker.internal:30104/mcp",
                "headers": {
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBleGFtcGxlLmNvbSIsImlzcyI6Im1jcGdhdGV3YXkiLCJhdWQiOiJtY3BnYXRld2F5LWFwaSIsImlhdCI6MTc2NjY4OTY0OCwianRpIjoiMzRlMDVkNWQtNmQ1Yy00OWFjLWI1OTgtZDAzZDdkODZmNWU1IiwidXNlciI6eyJlbWFpbCI6ImFkbWluQGV4YW1wbGUuY29tIiwiZnVsbF9uYW1lIjoiQVBJIFRva2VuIFVzZXIiLCJpc19hZG1pbiI6dHJ1ZSwiYXV0aF9wcm92aWRlciI6ImFwaV90b2tlbiJ9LCJ0ZWFtcyI6W10sIm5hbWVzcGFjZXMiOlsidXNlcjphZG1pbkBleGFtcGxlLmNvbSIsInB1YmxpYyJdLCJleHAiOjE3NjkyODE2NDgsInNjb3BlcyI6eyJzZXJ2ZXJfaWQiOiIyMzdiOGU2YjhjOWU0N2E1YWI1OWIxZWY2ZjdhMDMzOSIsInBlcm1pc3Npb25zIjpbIioiXSwiaXBfcmVzdHJpY3Rpb25zIjpbXSwidGltZV9yZXN0cmljdGlvbnMiOnt9fX0.FHQ2u4sbm-2aZwE8KARM9ZRyYLtZ2cSqCElXFQcmM0M",
                    "Accept": "application/json"
                }
            }
        }
    )
    
    tools = await client.get_tools()
    print("可用的工具:", [t.name for t in tools])

    llm = ChatOllama(
        model="gpt-oss:20b",
        temperature=0,
        base_url=server_url,
    )
    agent = create_agent(
        llm,
        tools=tools,
        system_prompt="You are a helpful assistant. Be concise and accurate."
    )

    result = await agent.ainvoke(
        {"messages": [HumanMessage("新竹今天天氣如何??")]}
    , config={"callbacks":[langfuse_handler]})
    
    print(result["messages"][-1].content)
    

asyncio.run(main())