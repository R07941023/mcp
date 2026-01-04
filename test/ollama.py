from typing import List

from langchain.messages import AIMessage
from langchain.tools import tool
from langchain_ollama import ChatOllama

server_url = 'http://host.docker.internal:11434'

@tool
def validate_user(user_id: int, addresses: List[str]) -> str:
    """Validate user using historical addresses."""
    if user_id == 123:
        return f"User {user_id} validated with addresses {', '.join(addresses)}."
    return "Validation failed."


llm = ChatOllama(
    model="gpt-oss:20b",
    validate_model_on_init=True,
    temperature=0,
    base_url=server_url,
).bind_tools([validate_user])

result = llm.invoke(
    "Could you validate user 123? They previously lived at "
    "123 Fake St in Boston MA and 234 Pretend Boulevard in "
    "Houston TX."
)

if isinstance(result, AIMessage) and result.tool_calls:
    print(result.tool_calls)
print(result)