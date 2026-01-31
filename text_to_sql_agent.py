"""
LangGraph-based Text-to-SQL Agent
This agent converts natural language questions to SQL queries and executes them.
"""
import os
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sample.db")
engine = create_engine(DATABASE_URL)


class AgentState(TypedDict):
    """State for the agent graph"""
    user_input: str
    database_schema: str
    sql_query: str
    query_result: str
    error: str
    messages: Sequence[HumanMessage | AIMessage | SystemMessage]


def get_database_schema() -> str:
    """Get the database schema information"""
    inspector = inspect(engine)
    schema_info = []
    
    for table_name in inspector.get_table_names():
        schema_info.append(f"\nTable: {table_name}")
        columns = inspector.get_columns(table_name)
        for column in columns:
            schema_info.append(f"  - {column['name']}: {column['type']}")
    
    return "\n".join(schema_info)


def generate_sql(state: AgentState) -> AgentState:
    """Node: Generate SQL from natural language"""
    print("🤖 Generating SQL query...")
    
    # Get database schema
    schema = get_database_schema()
    state["database_schema"] = schema
    
    # Create LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a SQL expert. Given a database schema and a user question, 
generate a valid SQL query to answer the question.

Database Schema:
{schema}

Rules:
1. Generate ONLY the SQL query, no explanations
2. Use proper SQL syntax
3. Make sure the query is safe (no DROP, DELETE, or UPDATE unless explicitly requested)
4. Return only SELECT queries unless the user explicitly requests modifications
"""),
        ("human", "{question}")
    ])
    
    # Generate SQL
    try:
        chain = prompt | llm
        response = chain.invoke({
            "schema": schema,
            "question": state["user_input"]
        })
        
        sql_query = response.content.strip()
        # Remove markdown code blocks if present
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        if sql_query.startswith("```"):
            sql_query = sql_query[3:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
        sql_query = sql_query.strip()
        
        state["sql_query"] = sql_query
        state["error"] = ""
        print(f"📝 Generated SQL: {sql_query}")
        
    except Exception as e:
        state["error"] = f"Error generating SQL: {str(e)}"
        print(f"❌ {state['error']}")
    
    return state


def execute_sql(state: AgentState) -> AgentState:
    """Node: Execute the SQL query"""
    print("🔄 Executing SQL query...")
    
    if state.get("error"):
        return state
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(state["sql_query"]))
            rows = result.fetchall()
            
            if rows:
                # Format results as a table
                columns = result.keys()
                result_lines = ["\t".join(columns)]
                for row in rows:
                    result_lines.append("\t".join(str(val) for val in row))
                state["query_result"] = "\n".join(result_lines)
                print(f"✅ Query executed successfully. Found {len(rows)} rows.")
            else:
                state["query_result"] = "Query executed successfully. No results returned."
                print("✅ Query executed successfully. No results.")
                
    except Exception as e:
        state["error"] = f"Error executing SQL: {str(e)}"
        state["query_result"] = ""
        print(f"❌ {state['error']}")
    
    return state


def format_output(state: AgentState) -> AgentState:
    """Node: Format the final output"""
    print("📋 Formatting output...")
    
    if state.get("error"):
        output = f"""
错误 / Error:
{state['error']}
"""
    else:
        output = f"""
用户问题 / User Question:
{state['user_input']}

生成的SQL / Generated SQL:
{state['sql_query']}

查询结果 / Query Results:
{state['query_result']}
"""
    
    state["final_output"] = output
    return state


def create_text_to_sql_agent():
    """Create the LangGraph agent"""
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
    
    return app


def run_query(user_input: str) -> str:
    """Run a text-to-SQL query"""
    agent = create_text_to_sql_agent()
    
    # Initial state
    initial_state = {
        "user_input": user_input,
        "database_schema": "",
        "sql_query": "",
        "query_result": "",
        "error": "",
        "messages": []
    }
    
    # Run the agent
    result = agent.invoke(initial_state)
    
    return result.get("final_output", "No output generated")


if __name__ == "__main__":
    # Example usage
    print("=" * 60)
    print("欢迎使用 LangGraph Text-to-SQL 智能体")
    print("Welcome to LangGraph Text-to-SQL Agent")
    print("=" * 60)
    
    # Test query
    test_question = "显示所有用户的信息 / Show all users"
    print(f"\n测试问题: {test_question}\n")
    
    output = run_query(test_question)
    print(output)
