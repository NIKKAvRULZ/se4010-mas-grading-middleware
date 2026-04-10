from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.tools.extraction_tool import extract_grades
from src.state import GradingBatch

def run_ingestion_agent(state: GradingBatch) -> dict:
    """Nithika's Component"""
    file_path = state.get("file_path", "data/sample_grades.xlsx")
    
    extracted_grades = extract_grades(file_path)
    
    try:
        llm = ChatOllama(model="phi3")
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an automated data ingestion script helping a university. Summarize the extraction action in one brief sentence."),
            ("human", f"I extracted {len(extracted_grades)} grading records from {file_path}. Write a 1-sentence log.")
        ])
        chain = prompt | llm
        log_msg = chain.invoke({}).content
    except Exception:
        print("⚠️ Ollama connection failed for Ingestion Agent.")
        log_msg = f"Extracted {len(extracted_grades)} records from {file_path} (Ollama failed)."
    
    return {
        "grades": extracted_grades,
        "logs": [f"Ingestion Agent: {log_msg}"]
    }
