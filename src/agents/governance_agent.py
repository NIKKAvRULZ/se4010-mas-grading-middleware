import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.tools.audit_tool import audit_grades, write_audit_log
from src.state import GradingBatch

def run_governance_agent(state: GradingBatch) -> dict:
    """Dilki's Component"""
    grades = state.get("grades", [])
    
    valid_grades, anomalies_found = audit_grades(grades)
    
    if anomalies_found:
        write_audit_log(anomalies_found)
        
    try:
        llm = ChatOllama(model="phi3")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an automated academic auditor. Summarize the audit findings in one very short sentence."),
            ("human", f"I audited the grades and found {len(valid_grades)} valid records and {len(anomalies_found)} anomalies. Write a 1-sentence log.")
        ])
        chain = prompt | llm
        log_msg = chain.invoke({}).content
    except Exception:
        print("⚠️ Ollama connection failed for Governance Agent.")
        log_msg = f"Found {len(valid_grades)} valid grades and {len(anomalies_found)} anomalies (Ollama failed)."
        
    return {
        "grades": valid_grades,
        "anomalies": anomalies_found,
        "logs": [f"Governance Agent: {log_msg}"]
    }
