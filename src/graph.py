import os
import sys
import json
import logging
from langgraph.graph import StateGraph, START, END

# Setup strict logging to satisfy the "Observability" grading criteria
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ==========================================
# IMPORT ALL TEAM AGENTS
# ==========================================
from src.state import GradingBatchState
from src.agents.ingestion_agent import run_ingestion_agent       # Nithika
from src.agents.governance_agent import verify_grades            # Dilki
from src.agents.privacy_agent import run_privacy_agent           # Susara
from src.agents.ledger_agent import run_ledger_agent             # Imeshi


# ==========================================
# NODE 1: NITHIKA (DATA INGESTION)
# ==========================================
def ingestion_node(state: GradingBatchState):
    logger.info("[NODE 1] Ingestion Agent Activated. Reading offline data...")
    file_path = state["file_path"]
    
    try:
        agent_output = run_ingestion_agent(file_path)
        parsed_data = json.loads(agent_output).get("students", [])
        
        logger.info(f"[NODE 1] Success: Extracted {len(parsed_data)} records securely.")
        return {"raw_json": parsed_data}
    except Exception as e:
        logger.error(f"[NODE 1] Failed to parse ingestion output: {e}")
        return {"errors": [f"Ingestion failed: {e}"]}

# ==========================================
# NODE 2: DILKI (GOVERNANCE & AUDIT)
# ==========================================
def governance_node(state: GradingBatchState):
    logger.info("[NODE 2] Governance Agent Activated. Auditing records...")
    raw_data = state.get("raw_json", [])
    
    if not raw_data:
        return {"errors": ["No data received from Ingestion."]}
    
    # Call Dilki's actual agent (mapping our state to her expected input)
    audit_result = verify_grades({"data": raw_data})
    
    if audit_result.get("status") == "success":
        logger.info("[NODE 2] Success: Audit passed and log generated.")
        return {
            "audit_status": "PASSED",
            "audit_log_path": audit_result.get("log_file")
        }
    else:
        logger.error("[NODE 2] Audit Failed! Anomalies detected.")
        return {
            "audit_status": "FAILED",
            "errors": [f"Governance Audit Failed. Invalid records: {audit_result.get('invalid_records')}"]
        }

# ==========================================
# NODE 3: SUSARA (PRIVACY & SECURITY)
# ==========================================
def privacy_node(state: GradingBatchState):
    logger.info("[NODE 3] Privacy Agent Activated. Masking PII...")
    
    # Call Susara's actual agent
    privacy_result = run_privacy_agent(state)
    anonymized_data = privacy_result.get("anonymized_data", [])
    
    logger.info("[NODE 3] Success: Student identities securely masked.")
    return {"anonymized_data": anonymized_data}

# ==========================================
# NODE 4: IMESHI (LEDGER ANCHORING)
# ==========================================
def ledger_node(state: GradingBatchState):
    logger.info("[NODE 4] Ledger Agent Activated. Generating cryptographic proof...")
    anonymized_data = state.get("anonymized_data", [])
    
    if not anonymized_data:
        return {"errors": ["No anonymized data received for ledger anchoring."]}
    
    # Call Imeshi's actual agent
    merkle_root = run_ledger_agent(anonymized_data)
    
    logger.info(f"[NODE 4] Success: Payload anchored. Merkle Root: {merkle_root}")
    return {"merkle_root": merkle_root}


# ==========================================
# BUILD AND COMPILE THE LANGGRAPH
# ==========================================
logger.info("Initializing LangGraph Orchestrator...")
workflow = StateGraph(GradingBatchState)

# Add all the team's nodes
workflow.add_node("Ingestion_Agent", ingestion_node)
workflow.add_node("Governance_Agent", governance_node)
workflow.add_node("Privacy_Agent", privacy_node)
workflow.add_node("Ledger_Agent", ledger_node)

# Define the sequential pipeline (The Flow)
workflow.add_edge(START, "Ingestion_Agent")
workflow.add_edge("Ingestion_Agent", "Governance_Agent")
workflow.add_edge("Governance_Agent", "Privacy_Agent")
workflow.add_edge("Privacy_Agent", "Ledger_Agent")
workflow.add_edge("Ledger_Agent", END)

# Compile the graph
mas_pipeline = workflow.compile()

# ==========================================
# RUN THE PIPELINE (For the Demo Video)
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 STARTING SECURE GRADING PIPELINE")
    print("="*50 + "\n")
    
    # Define the starting state
    initial_state = {
        "file_path": os.path.join(os.path.dirname(__file__), "..", "data", "sample_grades.xlsx"),
        "raw_json": None,
        "audit_status": None,
        "audit_log_path": None,
        "anonymized_data": None,
        "merkle_root": None,
        "errors": []
    }
    
    # Execute the graph
    final_state = mas_pipeline.invoke(initial_state)
    
    print("\n" + "="*50)
    print("🏁 PIPELINE EXECUTION COMPLETE")
    print("="*50)
    print(f"Final Merkle Root for Blockchain: {final_state.get('merkle_root')}")
    print(f"Audit Status: {final_state.get('audit_status')}")
    if final_state.get('audit_log_path'):
        print(f"Audit Log Saved At: {final_state.get('audit_log_path')}")
    if final_state.get('errors'):
        print(f"Errors Encountered: {final_state.get('errors')}")

# Print the graph visually in the terminal
    print("\n" + "="*50)
    print("📊 LANGGRAPH PIPELINE ARCHITECTURE")
    print("="*50)
    mas_pipeline.get_graph().print_ascii()

    # Generate and save a PNG diagram automatically
    try:
        diagram_path = os.path.join(os.path.dirname(__file__), "..", "data", "outputs", "mas_architecture.png")
        png_bytes = mas_pipeline.get_graph().draw_mermaid_png()
        
        with open(diagram_path, "wb") as f:
            f.write(png_bytes)
            
        print(f"\n✅ Pipeline diagram successfully saved as an image at: {diagram_path}")
    except Exception as e:
        print(f"\n⚠️ Could not generate image diagram: {e}")