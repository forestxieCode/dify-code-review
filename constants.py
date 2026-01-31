"""
Constants used throughout the Text-to-SQL agent.

This module centralizes all constant values to improve
maintainability and avoid magic strings/numbers.
"""

# SQL Query Types
QUERY_TYPE_SELECT = "SELECT"
QUERY_TYPE_INSERT = "INSERT"
QUERY_TYPE_UPDATE = "UPDATE"
QUERY_TYPE_DELETE = "DELETE"
QUERY_TYPE_DROP = "DROP"

# Dangerous SQL operations (blocked by default)
DANGEROUS_OPERATIONS = [
    QUERY_TYPE_DROP,
    QUERY_TYPE_DELETE,
    QUERY_TYPE_UPDATE,
    "TRUNCATE",
    "ALTER",
]

# System Messages
SYSTEM_PROMPT_SQL_GENERATION = """You are a SQL expert. Given a database schema and a user question, 
generate a valid SQL query to answer the question.

Database Schema:
{schema}

Rules:
1. Generate ONLY the SQL query, no explanations
2. Use proper SQL syntax
3. Make sure the query is safe (no DROP, DELETE, or UPDATE unless explicitly requested)
4. Return only SELECT queries unless the user explicitly requests modifications
"""

# Output Formatting
OUTPUT_SEPARATOR = "=" * 80
OUTPUT_SUBSEPARATOR = "-" * 80
OUTPUT_TAB = "\t"

# Messages
MSG_GENERATING_SQL = "🤖 Generating SQL query..."
MSG_EXECUTING_SQL = "🔄 Executing SQL query..."
MSG_FORMATTING_OUTPUT = "📋 Formatting output..."
MSG_QUERY_SUCCESS = "✅ Query executed successfully. Found {count} rows."
MSG_QUERY_NO_RESULTS = "✅ Query executed successfully. No results returned."
MSG_ERROR_PREFIX = "❌ "

# CLI Messages
CLI_WELCOME = "🤖 LangGraph Text-to-SQL 智能体 / LangGraph Text-to-SQL Agent"
CLI_GOODBYE = "👋 再见! / Goodbye!"
CLI_PROMPT = "💬 请输入你的问题 / Enter your question: "
CLI_EXIT_COMMANDS = ['quit', 'exit', '退出']

# Error Messages
ERR_GENERATING_SQL = "Error generating SQL: {error}"
ERR_EXECUTING_SQL = "Error executing SQL: {error}"
ERR_INVALID_CONFIG = "Invalid configuration: {error}"
ERR_DATABASE_CONNECTION = "Database connection error: {error}"

# Markdown code block markers
MARKDOWN_SQL_START = "```sql"
MARKDOWN_CODE_START = "```"
MARKDOWN_CODE_END = "```"
