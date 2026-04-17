import os
import sys
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.tools.masking_tool import mask_pii

def run_privacy_agent(state: dict) -> dict:
    """
    LangGraph node function for the Privacy Validation Agent.
    """
    print("\n[PRIVACY AGENT] Validating and anonymizing records...")
    
    # 1. Aligned with the LangGraph state.py keys
    raw_data = state.get("raw_json", [])
    
    # 2. Apply the cryptographic masking tool
    anonymized_data = mask_pii(raw_data)
    
    # 3. Use ChatOllama to generate a privacy compliance report
    try:
        llm = ChatOllama(model="phi3", temperature=0) 
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a strict data privacy auditor. Summarize the anonymization action in exactly one short sentence."),
            ("human", f"I successfully hashed the PII for {len(anonymized_data)} records. Provide a formal audit log entry.")
        ])
        
        chain = prompt | llm
        privacy_status_log = chain.invoke({}).content
        print(f"[PRIVACY LOG]: {privacy_status_log}")
        
    except Exception as e:
        print(f"⚠️ Ollama connection failed: {e}")
    
    # 4. Return the newly anonymized data back to the LangGraph state
    return {
        "anonymized_data": anonymized_data
    }