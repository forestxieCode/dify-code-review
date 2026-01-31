"""
Database operations for the Text-to-SQL agent.

This module encapsulates all database-related functionality,
including schema retrieval and query execution.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, text, inspect, Engine
from sqlalchemy.exc import SQLAlchemyError

from config import config
from exceptions import DatabaseError, SchemaRetrievalError, SQLExecutionError, UnsafeQueryError
from logger import logger
from constants import DANGEROUS_OPERATIONS


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize the database manager.
        
        Args:
            database_url: Optional database URL. If not provided, uses config.
        """
        self._database_url = database_url or config.database.url
        self._engine: Optional[Engine] = None
        self._cached_schema: Optional[str] = None
    
    @property
    def engine(self) -> Engine:
        """
        Get or create the database engine.
        
        Returns:
            SQLAlchemy engine instance
        """
        if self._engine is None:
            try:
                self._engine = create_engine(
                    self._database_url,
                    echo=config.database.echo,
                    pool_size=config.database.pool_size,
                    max_overflow=config.database.max_overflow
                )
                logger.info(f"Database engine created for: {self._database_url}")
            except SQLAlchemyError as e:
                logger.error(f"Failed to create database engine: {e}")
                raise DatabaseError(f"Database connection error: {e}")
        
        return self._engine
    
    def get_schema(self, use_cache: bool = True) -> str:
        """
        Retrieve the database schema information.
        
        Args:
            use_cache: Whether to use cached schema if available
            
        Returns:
            String representation of the database schema
            
        Raises:
            SchemaRetrievalError: If schema cannot be retrieved
        """
        if use_cache and self._cached_schema and config.agent.cache_schema:
            logger.debug("Using cached database schema")
            return self._cached_schema
        
        try:
            inspector = inspect(self.engine)
            schema_parts = []
            
            table_names = inspector.get_table_names()
            logger.info(f"Retrieved {len(table_names)} tables from database")
            
            for table_name in table_names:
                schema_parts.append(f"\nTable: {table_name}")
                columns = inspector.get_columns(table_name)
                
                for column in columns:
                    column_info = f"  - {column['name']}: {column['type']}"
                    # Add NOT NULL constraint if column is not nullable
                    if column.get('nullable') is False:
                        column_info += " NOT NULL"
                    schema_parts.append(column_info)
            
            schema = "\n".join(schema_parts)
            
            # Cache the schema
            if config.agent.cache_schema:
                self._cached_schema = schema
                logger.debug("Schema cached successfully")
            
            return schema
            
        except SQLAlchemyError as e:
            logger.error(f"Failed to retrieve database schema: {e}")
            raise SchemaRetrievalError(f"Schema retrieval error: {e}")
    
    def execute_query(
        self,
        sql_query: str,
        check_safety: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results.
        
        Args:
            sql_query: The SQL query to execute
            check_safety: Whether to check if query is safe
            
        Returns:
            List of dictionaries representing query results
            
        Raises:
            UnsafeQueryError: If query contains dangerous operations
            SQLExecutionError: If query execution fails
        """
        if check_safety and not self._is_safe_query(sql_query):
            logger.warning(f"Unsafe query blocked: {sql_query[:100]}")
            raise UnsafeQueryError(
                "Query contains potentially dangerous operations. "
                "Only SELECT queries are allowed by default."
            )
        
        try:
            with self.engine.connect() as conn:
                logger.debug(f"Executing query: {sql_query[:200]}")
                result = conn.execute(text(sql_query))
                
                # Fetch all rows and convert to list of dicts
                rows = result.fetchall()
                columns = result.keys()
                
                results = [
                    dict(zip(columns, row))
                    for row in rows
                ]
                
                logger.info(f"Query executed successfully. Retrieved {len(results)} rows")
                return results
                
        except SQLAlchemyError as e:
            logger.error(f"Query execution failed: {e}")
            raise SQLExecutionError(f"Error executing SQL: {e}")
    
    def _is_safe_query(self, sql_query: str) -> bool:
        """
        Check if a SQL query is safe to execute.
        
        Args:
            sql_query: The SQL query to check
            
        Returns:
            True if query is safe, False otherwise
        """
        query_upper = sql_query.upper().strip()
        
        # Check for dangerous operations
        for operation in DANGEROUS_OPERATIONS:
            if operation in query_upper:
                return False
        
        return True
    
    def clear_cache(self) -> None:
        """Clear the cached schema."""
        self._cached_schema = None
        logger.debug("Schema cache cleared")
    
    def close(self) -> None:
        """Close the database connection."""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            logger.info("Database connection closed")


# Global database manager instance
db_manager = DatabaseManager()
