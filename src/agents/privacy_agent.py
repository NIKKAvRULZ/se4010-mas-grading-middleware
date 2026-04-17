from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.tools.masking_tool import mask_pii
from src.state import GradingBatch

def run_privacy_agent(state: GradingBatch) -> dict:
    """
    LangGraph node function for the Privacy Validation Agent (Susara's Component).
    
    This agent takes the 'GradingBatch' state from the Governance Agent, 
    anonymizes the PII to ensure privacy, and uses a local Ollama LLM to
    generate a compliance summary before passing it to the Ledger Agent.
    """
    
    # 1. Extract the current batch of grades from the state
    grades_list = state.get("grades", [])
    
    # 2. Apply the cryptographic masking tool to the data
    anonymized_data = mask_pii(grades_list)
    
    # 3. Use ChatOllama to generate a privacy compliance report based on the action taken
    try:
        # Initialize local Ollama model (llama3 or phi3 as per README)
        llm = ChatOllama(model="phi3") # You can change this to "llama3" if installed
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a data privacy auditor for a university. Summarize the anonymization action in one short sentence."),
            ("human", f"I just hashed the names and student IDs for {len(anonymized_data)} records to ensure FERPA/GDPR compliance. Provide a direct 1-sentence log entry affirming this.")
        ])
        
        chain = prompt | llm
        privacy_status_log = chain.invoke({}).content
        
    except Exception as e:
        # Fallback if Ollama isn't running
        print("⚠️ Ollama connection failed. Is the model downloaded and running?")
        privacy_status_log = f"Anonymized {len(anonymized_data)} records via local hashing (Ollama failed)."
    
    # 4. Return the updated state
    return {
        "grades": anonymized_data,
        "privacy_status": "Anonymized via SHA-256",
        "logs": [f"Privacy Agent: {privacy_status_log}"]
    }
