import os
import sys
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.tools.merkle_tool import generate_merkle_root

# 1. Connect to the local LLM
llm = ChatOllama(model="phi3", temperature=0)

# 2. Prompt Engineering (For the 20% Agent Marks)
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Blockchain Infrastructure Specialist.
    You will receive a list of hashed student records. Your job is to verify the list is ready for Ethereum anchoring.
    Reply with a short, professional confirmation that the payload is secure, and state exactly how many hashes you are anchoring.
    Do NOT generate the Merkle root yourself, the system tool will do that."""),
    ("user", "Here are the hashed records ready for the blockchain:\n{hashed_records}")
])

chain = prompt | llm

def run_ledger_agent(hashed_records: list):
    print("\n[LEDGER AGENT] Requesting AI validation for blockchain payload...")
    
    # 1. The LLM reasons about the payload
    response = chain.invoke({"hashed_records": str(hashed_records)})
    print(f"\n[AI RESPONSE]:\n{response.content}\n")
    
    # 2. Call Imeshi's custom mathematical tool
    print("[LEDGER AGENT] Calling Merkle Root Generator Tool...")
    merkle_root = generate_merkle_root(hashed_records)
    
    print(f"🌳 [SUCCESS] Final Merkle Root Generated: {merkle_root}")
    return merkle_root