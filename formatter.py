"""
Output formatting utilities for the Text-to-SQL agent.

This module provides utilities for formatting query results
and other outputs in a user-friendly way.
"""
from typing import List, Dict, Any, Optional

from constants import OUTPUT_TAB


class OutputFormatter:
    """Formats query results and outputs."""
    
    @staticmethod
    def format_table(
        results: List[Dict[str, Any]],
        max_col_width: int = 50
    ) -> str:
        """
        Format query results as a table.
        
        Args:
            results: List of dictionaries representing rows
            max_col_width: Maximum width for column values
            
        Returns:
            Formatted table string
        """
        if not results:
            return "No results returned."
        
        # Get column names from first row
        columns = list(results[0].keys())
        
        # Build table
        lines = [OUTPUT_TAB.join(columns)]
        
        for row in results:
            formatted_values = [
                OutputFormatter._format_value(row.get(col), max_col_width)
                for col in columns
            ]
            lines.append(OUTPUT_TAB.join(formatted_values))
        
        return "\n".join(lines)
    
    @staticmethod
    def format_query_output(
        user_input: str,
        sql_query: str,
        results: List[Dict[str, Any]],
        error: Optional[str] = None
    ) -> str:
        """
        Format the complete query output.
        
        Args:
            user_input: Original user question
            sql_query: Generated SQL query
            results: Query results
            error: Error message if any
            
        Returns:
            Formatted output string
        """
        if error:
            return f"""
错误 / Error:
{error}
"""
        
        table_output = OutputFormatter.format_table(results)
        
        return f"""
用户问题 / User Question:
{user_input}

生成的SQL / Generated SQL:
{sql_query}

查询结果 / Query Results:
{table_output}
"""
    
    @staticmethod
    def _format_value(value: Any, max_width: int) -> str:
        """
        Format a single value for display.
        
        Args:
            value: Value to format
            max_width: Maximum width for the value
            
        Returns:
            Formatted string value
        """
        str_value = str(value) if value is not None else "NULL"
        
        # Ensure max_width is reasonable before truncating
        if max_width < 3:
            max_width = 3
        
        # Truncate if too long
        if len(str_value) > max_width:
            str_value = str_value[:max_width-3] + "..."
        
        return str_value
    
    @staticmethod
    def format_error(error: str, context: Optional[str] = None) -> str:
        """
        Format an error message.
        
        Args:
            error: Error message
            context: Optional context information
            
        Returns:
            Formatted error message
        """
        if context:
            return f"❌ Error ({context}): {error}"
        return f"❌ Error: {error}"
    
    @staticmethod
    def format_success(message: str, count: Optional[int] = None) -> str:
        """
        Format a success message.
        
        Args:
            message: Success message
            count: Optional count of results
            
        Returns:
            Formatted success message
        """
        if count is not None:
            return f"✅ {message} ({count} results)"
        return f"✅ {message}"
