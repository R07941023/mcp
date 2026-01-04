from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os


os.environ["OPENAI_API_KEY"]=os.getenv("LITELLM_API_KEY")

llm = ChatOpenAI(
    openai_api_base="https://litellm.mydormroom.dpdns.org",
    model = "gpt-oss:20b",
)

messages = [
    ("human", "你知道三眼章魚嗎"),
]
ai_msg = llm.invoke(messages)

print(ai_msg)