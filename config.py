"""
Configuration management for the Text-to-SQL agent.

This module centralizes all configuration settings and provides
a clean interface for accessing them.
"""
import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass(frozen=True)
class DatabaseConfig:
    """Database configuration settings."""
    url: str
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


@dataclass(frozen=True)
class LLMConfig:
    """Language Model configuration settings."""
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    api_key: Optional[str] = None


@dataclass(frozen=True)
class AgentConfig:
    """Agent configuration settings."""
    max_retries: int = 3
    query_timeout: int = 30  # seconds
    cache_schema: bool = True


class Config:
    """Main configuration class."""
    
    def __init__(self):
        """Initialize configuration from environment variables."""
        self.database = DatabaseConfig(
            url=os.getenv("DATABASE_URL", "sqlite:///./sample.db"),
            echo=os.getenv("DATABASE_ECHO", "false").lower() == "true"
        )
        
        self.llm = LLMConfig(
            model_name=os.getenv("LLM_MODEL", "gpt-3.5-turbo"),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.0")),
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.agent = AgentConfig(
            max_retries=int(os.getenv("AGENT_MAX_RETRIES", "3")),
            query_timeout=int(os.getenv("AGENT_QUERY_TIMEOUT", "30")),
            cache_schema=os.getenv("AGENT_CACHE_SCHEMA", "true").lower() == "true"
        )
    
    def validate(self) -> bool:
        """
        Validate configuration settings.
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        if not self.database.url:
            return False
        
        # Temperature must be between 0 and 2 (OpenAI API requirement)
        # 0 = deterministic, 1 = balanced, 2 = maximum creativity
        if self.llm.temperature < 0 or self.llm.temperature > 2:
            return False
        
        if self.agent.max_retries < 0:
            return False
        
        return True


# Global configuration instance
config = Config()
