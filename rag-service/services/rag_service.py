"""
RAG Service
"""
import logging
import json
import asyncpg

from .llm_client import LLMClient

logger = logging.getLogger(__name__)

class RAGService:
    """
    Service for handling Retrieval-Augmented Generation (RAG) operations.

    This service coordinates between the LLM client for embedding generation 
    and the PostgreSQL database for vector similarity searching.
    """
    def __init__(self, db_pool: asyncpg.Pool, llm_client: LLMClient):
        self.db_pool = db_pool
        self.llm_client = llm_client

    async def retrieve_rag_context(self, prompt: str, user_id: int) -> str:
        """
        Generates embeddings for the prompt and retrieves relevant context from the 
        PostgreSQL database using vector similarity search.
        """
        if not self.db_pool or not self.llm_client:
            logger.warning("Database pool or LLM client not available, skipping RAG retrieval.")
            return ""

        try:
            query_embedding = await self.llm_client.generate_embedding(prompt)

            async with self.db_pool.acquire() as connection:
                sql_query = """
                    SELECT d.content, e.embedding <=> $1::vector AS similarity
                    FROM embeddings e
                    JOIN documents d ON e.document_id = d.id
                    WHERE e.user_id = $2
                    ORDER BY similarity ASC
                    LIMIT 3;
                """
                rows = await connection.fetch(sql_query, json.dumps(query_embedding), user_id)

                if not rows:
                    logger.info("No RAG context found for prompt: %s, user_id: %s", prompt, user_id)
                    return ""

                return ",".join([row['content'] for row in rows])

        except asyncpg.PostgresError as pg_err:
            logger.error("Database error during RAG retrieval: %s", pg_err)
            return ""
