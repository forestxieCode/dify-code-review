"""
SQL generation using Language Models.

This module handles the interaction with LLMs to generate
SQL queries from natural language.
Supports both OpenAI and DeepSeek (OpenAI-compatible) APIs.
"""
from typing import Protocol, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel

from ..utils.config import config
from ..utils.exceptions import SQLGenerationError
from ..utils.logger import logger
from ..utils.constants import SYSTEM_PROMPT_SQL_GENERATION, MARKDOWN_SQL_START, MARKDOWN_CODE_START, MARKDOWN_CODE_END


class SQLGenerator(Protocol):
    """Protocol for SQL generator implementations."""
    
    def generate(self, question: str, schema: str) -> str:
        """Generate SQL from question and schema."""
        ...


class LLMSQLGenerator:
    """SQL generator using Language Models (supports OpenAI and DeepSeek)."""
    
    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize the SQL generator.
        
        Args:
            model_name: Name of the LLM model to use
            temperature: Temperature for generation
            api_key: API key (DeepSeek or OpenAI)
            base_url: Base URL for API (for DeepSeek or custom endpoints)
        """
        self.model_name = model_name or config.llm.model_name
        self.temperature = temperature if temperature is not None else config.llm.temperature
        self.api_key = api_key or config.llm.api_key
        self.base_url = base_url or config.llm.base_url
        
        self._llm: Optional[BaseLanguageModel] = None
        self._prompt: Optional[ChatPromptTemplate] = None
    
    @property
    def llm(self) -> BaseLanguageModel:
        """
        Get or create the language model instance.
        
        Returns:
            Initialized language model
        """
        if self._llm is None:
            # Build kwargs for ChatOpenAI
            llm_kwargs = {
                "model": self.model_name,
                "temperature": self.temperature,
                "openai_api_key": self.api_key
            }
            
            # Add base_url if provided (for DeepSeek or custom endpoints)
            # Note: Different versions of langchain-openai may use different parameter names
            if self.base_url:
                # Try both parameter names for compatibility
                llm_kwargs["openai_api_base"] = self.base_url
                logger.info(f"Using custom API base URL: {self.base_url}")
            
            self._llm = ChatOpenAI(**llm_kwargs)
            logger.info(f"LLM initialized: {self.model_name}")
        
        return self._llm
    
    @property
    def prompt(self) -> ChatPromptTemplate:
        """
        Get or create the prompt template.
        
        Returns:
            Prompt template for SQL generation
        """
        if self._prompt is None:
            self._prompt = ChatPromptTemplate.from_messages([
                ("system", SYSTEM_PROMPT_SQL_GENERATION),
                ("human", "{question}")
            ])
        
        return self._prompt
    
    def generate(self, question: str, schema: str) -> str:
        """
        Generate SQL query from natural language question.
        
        Args:
            question: User's natural language question
            schema: Database schema information
            
        Returns:
            Generated SQL query
            
        Raises:
            SQLGenerationError: If SQL generation fails
        """
        try:
            logger.debug(f"Generating SQL for question: {question}")
            
            chain = self.prompt | self.llm
            response = chain.invoke({
                "schema": schema,
                "question": question
            })
            
            sql_query = self._clean_sql_response(response.content)
            logger.info(f"SQL generated successfully: {sql_query[:100]}")
            
            return sql_query
            
        except Exception as e:
            logger.error(f"SQL generation failed: {e}")
            raise SQLGenerationError(f"Error generating SQL: {e}")
    
    def _clean_sql_response(self, response: str) -> str:
        """
        Clean the SQL response from the LLM.
        
        Removes markdown code blocks and extra whitespace.
        
        Args:
            response: Raw response from LLM
            
        Returns:
            Cleaned SQL query
        """
        sql_query = response.strip()
        
        # Remove markdown SQL code blocks
        if sql_query.startswith(MARKDOWN_SQL_START):
            sql_query = sql_query[len(MARKDOWN_SQL_START):]
        elif sql_query.startswith(MARKDOWN_CODE_START):
            sql_query = sql_query[len(MARKDOWN_CODE_START):]
        
        if sql_query.endswith(MARKDOWN_CODE_END):
            sql_query = sql_query[:-len(MARKDOWN_CODE_END)]
        
        return sql_query.strip()


class MockSQLGenerator:
    """Mock SQL generator for testing without API key."""
    
    def generate(self, question: str, schema: str) -> str:
        """
        Generate a mock SQL query.
        
        Args:
            question: User's question (unused in mock)
            schema: Database schema (unused in mock)
            
        Returns:
            Mock SQL query
        """
        logger.warning("Using mock SQL generator - results may not be accurate")
        return "SELECT * FROM users LIMIT 5"


def create_sql_generator(use_mock: bool = False) -> SQLGenerator:
    """
    Factory function to create SQL generator.
    
    Args:
        use_mock: If True, creates mock generator for testing
        
    Returns:
        SQL generator instance
    """
    if use_mock:
        logger.info("Creating mock SQL generator")
        return MockSQLGenerator()
    
    logger.info("Creating LLM-based SQL generator")
    return LLMSQLGenerator()
