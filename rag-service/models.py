"""
model
"""
from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    Schema for an incoming chat completion request.

    Attributes:
        prompt (str): The input text or instruction provided by the user.
    """
    prompt: str

class Document(BaseModel):
    """
    Schema representing a stored text document.

    Attributes:
        id (int): Unique identifier for the document record.
        content (str): The raw text content of the document.
        user_id (int): The identifier of the user who owns this document.
    """
    id: int
    content: str
    user_id: int

class Embedding(BaseModel):
    """
    Schema for vector embeddings associated with documents.

    Attributes:
        id (int): Unique identifier for the embedding record.
        document_id (int): Reference to the parent document.
        user_id (int): The identifier of the owner for access control.
        embedding (list[float]): The high-dimensional vector data.
    """
    id: int
    document_id: int
    user_id: int
    embedding: list[float]
    