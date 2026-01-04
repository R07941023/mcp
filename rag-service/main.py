"""
RAG Service
"""

import logging
from fastapi import Body, FastAPI, Header, Depends
import asyncpg
from utils.auth import get_service_account
from models import ChatRequest
from config import settings
from services.llm_client import LLMClient
from services.rag_service import RAGService

# --- App State ---


class AppState:
    """
    Global application state container.

    This class manages the lifecycle of shared resources, including
    database connections, LLM clients, and business logic services.

    Attributes:
        db_pool (asyncpg.Pool): The PostgreSQL connection pool.
        llm_client (LLMClient): Client for interfacing with the LLM (e.g., Ollama).
        rag_service (RAGService): Service for Retrieval-Augmented Generation.
        user_id (int): The current session's authenticated user identifier.
    """

    db_pool: asyncpg.Pool = None
    llm_client: LLMClient = None
    rag_service: RAGService = None
    user_id: int = None


app_state = AppState()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event("startup")
async def startup():
    """
    Handle application lifecycle events.

    Initializes the LLM client, database pool, and RAG service on startup.
    Ensures all resources, especially the database pool, are closed on shutdown.
    """
    logger.info("Starting up application...")
    try:
        # Initialize LLM Client
        app_state.llm_client = LLMClient(
            host=settings.ollama_endpoint, embedding_model=settings.embedding_model
        )
        logger.info(
            "Ollama client initialized for endpoint: %s", settings.ollama_endpoint
        )

        # Initialize Database Pool
        app_state.db_pool = await asyncpg.create_pool(settings.postgres_uri)
        logger.info("Database connection pool created successfully.")

        # Initialize RAG Service
        app_state.rag_service = RAGService(app_state.db_pool, app_state.llm_client)
        logger.info("RAG service initialized.")

    except Exception as e:
        logger.error("Failed during startup: %s", e, exc_info=True)
        # Optionally, re-raise or handle to prevent app from starting in a bad state
        raise


@app.on_event("shutdown")
async def shutdown():
    """
    Handle application shutdown tasks.

    Closes the database connection pool to ensure all resources
    are released properly before the process exits.
    """
    if app_state.db_pool:
        await app_state.db_pool.close()
        logger.info("Database connection pool closed.")


def get_rag_service() -> RAGService:
    """
    Dependency provider for the RAGService instance.

    Returns:
        RAGService: The global RAG service managed by the application state.
    """
    return app_state.rag_service


async def get_user_name(authorization: str | None = Header(default=None)) -> str:
    """
    Extract the user name or service account identity from the authorization header.

    Args:
        authorization (str | None): The raw Authorization header string.

    Returns:
        str: The identified service account name or an empty string if unauthorized.
    """
    return get_service_account(authorization) if authorization else ""


async def get_query_id(query_name: str = Body(..., embed=True)) -> str:
    """
    Fetch the internal database user ID based on a unique username.

    Args:
        username (str): The unique identifier/username to search for.

    Returns:
        int: The user's database ID if found, otherwise returns -1.
    """
    async with app_state.db_pool.acquire() as connection:
        result = await connection.fetchrow(
            "SELECT id FROM users WHERE username = $1;", query_name
        )
        return result["id"] if result else -1


@app.post("/query")
async def query(
    request: ChatRequest,
    query_id: str = Depends(get_query_id),
    user: str = Depends(get_user_name),
    rag_service: RAGService = Depends(get_rag_service),
):
    """RAG query"""
    logger.info("User=%s", user)
    response = await rag_service.retrieve_rag_context(request.prompt, query_id)
    return response
