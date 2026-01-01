"Auth process"
import logging
from typing import Tuple, Optional
import jwt

logger = logging.getLogger(__name__)

def get_service_account(authorization: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Decodes a JWT from an Authorization header to extract user name and email.

    Args:
        authorization: The content of the Authorization header (e.g., "Bearer <token>").

    Returns:
        A tuple containing (name, email). Returns (None, None) if the token
        cannot be decoded or the claims are not present.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None, None

    token = authorization.split(" ")[1]
    try:
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        service_account = decoded_token.get("preferred_username")
        logger.info("JWT decoded successfully.")
        return service_account

    except jwt.PyJWTError as e:
        logger.error("Error decoding JWT: %s", e)
        return None
