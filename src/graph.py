import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, START, END
import pprint

# Import State
from src.state import GradingBatch

# Import Agents (Nodes)
from src.agents.ingestion_agent import run_ingestion_agent
from src.agents.governance_agent import run_governance_agent
from src.agents.privacy_agent import run_privacy_agent
from src.agents.ledger_agent import run_ledger_agent

def compile_graph():
    """
    Main LangGraph orchestrator linking the sequential MAS pipeline.
    """
    
    # 1. Initialize State Graph
    workflow = StateGraph(GradingBatch)

    # 2. Add Nodes (Each Student's Agent)
    workflow.add_node("IngestionAgent", run_ingestion_agent)   # Nithika
    workflow.add_node("GovernanceAgent", run_governance_agent) # Dilki
    workflow.add_node("PrivacyAgent", run_privacy_agent)       # Susara
    workflow.add_node("LedgerAgent", run_ledger_agent)         # Imeshi
    
    # 3. Define the Edges (Control Flow)
    workflow.add_edge(START, "IngestionAgent")
    workflow.add_edge("IngestionAgent", "GovernanceAgent")
    workflow.add_edge("GovernanceAgent", "PrivacyAgent")
    workflow.add_edge("PrivacyAgent", "LedgerAgent")
    workflow.add_edge("LedgerAgent", END)

    # 4. Compile process
    app = workflow.compile()
    return app

if __name__ == "__main__":
    print("🚀 Initializing Secure Academic Grading MAS Middleware...")
    
    app = compile_graph()
    
    # Example input state
    initial_state = {
        "file_path": "data/sample_grades.xlsx",
        "grades": [],
        "anomalies": [],
        "privacy_status": "",
        "merkle_root": "",
        "logs": []
    }
    
    print("\n--- Workflow Execution Started ---\n")
    final_state = app.invoke(initial_state)
    
    print("\n--- Final Graph State ---\n")
    pprint.pprint(final_state)
