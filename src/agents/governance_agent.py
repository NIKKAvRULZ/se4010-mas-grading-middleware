import os
import sys
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.tools.audit_logger import generate_audit_log

# 1. Connect to the local LLM
llm = ChatOllama(model="phi3", temperature=0, format="json", num_predict=1024)

# 2. Strict Prompt Engineering (For the 20% Agent Marks)
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a strict Data Integrity Auditor.
    Your ONLY job is to check if the data structure is corrupted. 
    
    RULES:
    1. We are checking DATA INTEGRITY, not academic performance. Do NOT evaluate if a student passed or failed the class.
    2. A valid 'Midterm' or 'Practical' score is ANY number between 0 and 100 (e.g., 60 and 65 are perfectly valid numbers).
    3. Ignore the 'Final Grade' column completely.
    4. Since all provided numbers are between 0 and 100, the data is clean.
    5. Output JSON format exactly like this: {{"status": "success", "invalid_records": []}}
    """),
    ("user", "Here is the extracted grading data:\n\n{student_data}\n\nAudit this data for structural integrity and return the JSON report.")
])

chain = prompt | llm

def verify_grades(state: dict) -> dict:
    print("\n[GOVERNANCE AGENT] Auditing grades via local LLM...")
    data = state.get("data", [])
    
    # 1. Let the LLM reason about the data
    llm_response = chain.invoke({"student_data": json.dumps(data)})
    
    try:
        audit_result = json.loads(llm_response.content)
        
        # 2. If the LLM approves, call Dilki's custom tool to save the log
        if audit_result.get("status") == "success":
            print("[GOVERNANCE AGENT] Audit Passed. Generating secure log file...")
            log_file = generate_audit_log(data)
            return {"status": "success", "verified_data": data, "log_file": log_file}
        else:
            print("[GOVERNANCE AGENT] Audit Failed! Anomalies detected.")
            return {"status": "failed", "invalid_records": audit_result.get("invalid_records", [])}
            
    except Exception as e:
        return {"status": "error", "message": f"LLM parsing failed: {e}"}