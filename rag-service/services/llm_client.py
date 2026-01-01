"""
LLM Client Module.
Provides a wrapper around the Ollama asynchronous client for embeddings 
and model interactions.
"""
from typing import List
import ollama

class LLMClient:
    """
    Asynchronous client for interacting with the Ollama LLM service.

    This client handles embedding generation and potentially other LLM 
    tasks using a remote or local Ollama host.
    """
    def __init__(self, host: str, embedding_model: str):
        self.client = ollama.AsyncClient(host=host)
        self.embedding_model = embedding_model

    async def generate_embedding(self, prompt: str) -> List[float]:
        """Generates embeddings for a given prompt."""
        resp = await self.client.embeddings(
            model=self.embedding_model,
            prompt=prompt
        )
        return resp["embedding"]
