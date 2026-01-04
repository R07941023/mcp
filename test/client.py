import asyncio
# from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage
from langfuse.langchain import CallbackHandler
from langfuse import Langfuse
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("LITELLM_API_KEY")
mcp_token = os.getenv("MCP_TOKEN")
langfuse = Langfuse()
langfuse_handler = CallbackHandler()

async def main():

    # prompt = langfuse.get_prompt("n8n", label="production")
    # print(prompt.get_langchain_prompt())

    # 1. 初始化 MCP Client 並取得工具定義
    client = MultiServerMCPClient(
        {
            "weather": {
                "transport": "streamable_http",
                "url": "http://host.docker.internal:30102/servers/fe5c6f8a05154a2eb5f04f691ec321a5/mcp",
                "headers": {
                    "Authorization": "Bearer " + mcp_token,
                    "Accept": "application/json"
                }
            }
        }
    )
    
    tools = await client.get_tools()
    print("可用的工具:", [t.name for t in tools])

    # llm = ChatOllama(
    #     model="gpt-oss:20b",
    #     temperature=0,
    #     base_url='http://host.docker.internal:11434',
    # )
    llm = ChatOpenAI(
        openai_api_base="https://litellm.mydormroom.dpdns.org",
        temperature=0,
        model = "gemini/gemini-2.5-flash",
    )
    agent = create_agent(
        llm,
        tools=tools,
        system_prompt="You are a helpful assistant. Be concise and accurate."
    )

    result = await agent.ainvoke(
        {"messages": [HumanMessage("台積電和聯發科的今天收盤價")]}
    , config={"callbacks":[langfuse_handler]})
    
    print(result["messages"][-1].content)
    

asyncio.run(main())