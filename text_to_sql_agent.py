"""
LangGraph-based Text-to-SQL Agent

This agent converts natural language questions to SQL queries and executes them.
Refactored for better code readability, maintainability, and extensibility.
"""
from typing import TypedDict, Sequence, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from database import db_manager
from sql_generator import create_sql_generator
from formatter import OutputFormatter
from logger import logger
from constants import (
    MSG_GENERATING_SQL,
    MSG_EXECUTING_SQL,
    MSG_FORMATTING_OUTPUT,
    MSG_QUERY_SUCCESS,
    MSG_QUERY_NO_RESULTS,
    MSG_ERROR_PREFIX
)
from exceptions import SQLGenerationError, SQLExecutionError


class AgentState(TypedDict):
    """
    State for the agent graph.
    
    Attributes:
        user_input: The user's natural language question
        database_schema: Database schema information
        sql_query: Generated SQL query
        query_results: Query execution results as list of dicts (List[Dict[str, Any]])
        error: Error message if any error occurred
        messages: Message history for conversation
        final_output: Formatted final output
    """
    user_input: str
    database_schema: str
    sql_query: str
    query_results: list  # List[Dict[str, Any]]
    error: str
    messages: Sequence[HumanMessage | AIMessage | SystemMessage]
    final_output: str


def generate_sql(state: AgentState) -> AgentState:
    """
    Node: Generate SQL from natural language.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated agent state with generated SQL
    """
    logger.info(MSG_GENERATING_SQL)
    
    try:
        # Get database schema
        schema = db_manager.get_schema()
        state["database_schema"] = schema
        
        # Create SQL generator
        sql_gen = create_sql_generator()
        
        # Generate SQL query
        sql_query = sql_gen.generate(
            question=state["user_input"],
            schema=schema
        )
        
        state["sql_query"] = sql_query
        state["error"] = ""
        logger.info(f"Generated SQL: {sql_query}")
        
    except SQLGenerationError as e:
        error_msg = f"{MSG_ERROR_PREFIX}{str(e)}"
        state["error"] = str(e)
        logger.error(error_msg)
    except Exception as e:
        error_msg = f"{MSG_ERROR_PREFIX}Unexpected error: {str(e)}"
        state["error"] = str(e)
        logger.exception("Unexpected error during SQL generation")
    
    return state


def execute_sql(state: AgentState) -> AgentState:
    """
    Node: Execute the SQL query.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated agent state with query results
    """
    logger.info(MSG_EXECUTING_SQL)
    
    # Skip execution if there was an error in previous step
    if state.get("error"):
        return state
    
    try:
        # Execute query using database manager
        results = db_manager.execute_query(state["sql_query"])
        
        state["query_results"] = results
        
        if results:
            msg = MSG_QUERY_SUCCESS.format(count=len(results))
            logger.info(msg)
        else:
            logger.info(MSG_QUERY_NO_RESULTS)
            
    except (SQLExecutionError, Exception) as e:
        error_msg = f"{MSG_ERROR_PREFIX}{str(e)}"
        state["error"] = str(e)
        state["query_results"] = []
        logger.error(error_msg)
    
    return state


def format_output(state: AgentState) -> AgentState:
    """
    Node: Format the final output.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated agent state with formatted output
    """
    logger.info(MSG_FORMATTING_OUTPUT)
    
    output = OutputFormatter.format_query_output(
        user_input=state["user_input"],
        sql_query=state.get("sql_query", ""),
        results=state.get("query_results", []),
        error=state.get("error")
    )
    
    state["final_output"] = output
    return state


def create_text_to_sql_agent() -> StateGraph:
    """
    Create the LangGraph agent workflow.
    
    Returns:
        Compiled LangGraph workflow
    """
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("generate_sql", generate_sql)
    workflow.add_node("execute_sql", execute_sql)
    workflow.add_node("format_output", format_output)
    
    # Add edges
    workflow.set_entry_point("generate_sql")
    workflow.add_edge("generate_sql", "execute_sql")
    workflow.add_edge("execute_sql", "format_output")
    workflow.add_edge("format_output", END)
    
    # Compile the graph
    app = workflow.compile()
    
    logger.debug("LangGraph workflow created successfully")
    return app


def run_query(user_input: str) -> str:
    """
    Run a text-to-SQL query.
    
    Args:
        user_input: Natural language question from user
        
    Returns:
        Formatted output string with results
    """
    logger.info(f"Running query: {user_input}")
    
    agent = create_text_to_sql_agent()
    
    # Initial state
    initial_state: AgentState = {
        "user_input": user_input,
        "database_schema": "",
        "sql_query": "",
        "query_results": [],
        "error": "",
        "messages": [],
        "final_output": ""
    }
    
    # Run the agent
    result = agent.invoke(initial_state)
    
    return result.get("final_output", "No output generated")


if __name__ == "__main__":
    # Example usage
    from constants import OUTPUT_SEPARATOR
    
    print(OUTPUT_SEPARATOR)
    print("欢迎使用 LangGraph Text-to-SQL 智能体")
    print("Welcome to LangGraph Text-to-SQL Agent")
    print(OUTPUT_SEPARATOR)
    
    # Test query
    test_question = "显示所有用户的信息 / Show all users"
    print(f"\n测试问题: {test_question}\n")
    
    output = run_query(test_question)
    print(output)
