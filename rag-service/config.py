"""
config
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings and environment variable configurations.

    This class uses pydantic-settings to load configuration from environment
    variables or a .env file. It centralizes all service endpoints and
    database credentials.
    """

    ollama_endpoint: str = "http://host.docker.internal:11434"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_name: str = "rag"
    embedding_model: str = "nomic-embed-text"

    @property
    def postgres_uri(self) -> str:
        """
        Construct the PostgreSQL DSN (Data Source Name) URI.

        Returns:
            str: A formatted connection string for asyncpg or other SQL clients.
        """

        return (
            f"postgres://{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_host}:{self.postgres_port}/{self.postgres_name}"
        )

    class Config:
        """
        Pydantic configuration for settings management.

        Defines how environment variables are loaded, including the file
        path and encoding settings.
        """

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
