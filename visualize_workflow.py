"""
Visualize the LangGraph workflow
"""
from langgraph.graph import StateGraph, END
from text_to_sql_agent import AgentState, generate_sql, execute_sql, format_output


def visualize_workflow():
    """Create and display the workflow graph"""
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
    
    print("LangGraph Workflow Structure:")
    print("=" * 60)
    print()
    print("  ┌─────────────────┐")
    print("  │   User Input    │")
    print("  └────────┬────────┘")
    print("           │")
    print("           ▼")
    print("  ┌─────────────────┐")
    print("  │  Generate SQL   │  ← Uses LLM (GPT-3.5) to convert")
    print("  │                 │    natural language to SQL")
    print("  └────────┬────────┘")
    print("           │")
    print("           ▼")
    print("  ┌─────────────────┐")
    print("  │  Execute SQL    │  ← Runs query on database")
    print("  │                 │    using SQLAlchemy")
    print("  └────────┬────────┘")
    print("           │")
    print("           ▼")
    print("  ┌─────────────────┐")
    print("  │ Format Output   │  ← Formats results as table")
    print("  │                 │")
    print("  └────────┬────────┘")
    print("           │")
    print("           ▼")
    print("  ┌─────────────────┐")
    print("  │  Final Result   │")
    print("  └─────────────────┘")
    print()
    print("=" * 60)
    print("\nWorkflow compiled successfully!")
    print(f"Number of nodes: {len(app.nodes)}")
    

if __name__ == "__main__":
    visualize_workflow()
