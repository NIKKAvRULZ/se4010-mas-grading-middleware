from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.tools.merkle_tool import create_merkle_root
from src.state import GradingBatch

def run_ledger_agent(state: GradingBatch) -> dict:
    """Imeshi's Component"""
    privacy_masked_grades = state.get("grades", [])
    
    root_hash = create_merkle_root(privacy_masked_grades)
    
    try:
        llm = ChatOllama(model="phi3")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a blockchain ledger anchoring agent tracking academic integrity. Summarize the hashing action in one very short sentence."),
            ("human", f"I secured the batch of records by generating this Merkle Root hash: {root_hash}. Write a 1-sentence log.")
        ])
        chain = prompt | llm
        log_msg = chain.invoke({}).content
    except Exception:
        print("⚠️ Ollama connection failed for Ledger Agent.")
        log_msg = f"Anchored Merkle Root: {root_hash} (Ollama failed)."
    
    return {
        "merkle_root": root_hash,
        "logs": [f"Ledger Agent: {log_msg}"]
    }
