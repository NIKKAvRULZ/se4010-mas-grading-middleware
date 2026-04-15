import os
import sys
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# Add the root directory to the system path so we can import your tool
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.tools.extraction_tool import extract_excel_grades

# 1. Define the LLM with Ollama's native JSON Mode enabled
llm = ChatOllama(model="phi3", temperature=0, format="json", num_predict=2048)

# 2. Design the Agent's Persona and Constraints
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a strict Academic Data Ingestion Specialist. 
    Your ONLY job is to receive raw dictionary data and format it into a clean JSON object.
    
    CRITICAL CONSTRAINTS:
    1. Output ONLY valid JSON.
    2. The JSON must be an object with a single key called "students" containing the array of records.
    3. NEVER alter, invent, or drop any grades or Student IDs.
    """),
    ("user", "Here is the raw data:\n\n{raw_data}\n\nReturn the JSON object.")
])

# 3. Create the LangChain processing chain
chain = prompt | llm

def run_ingestion_agent(file_path: str):
    """
    Orchestrates the ingestion workflow: Calls the tool, then passes the data to the LLM.
    """
    print(f"\n[AGENT WORKFLOW] Starting Ingestion Process for: {file_path}")
    
    # Step 1: The Agent utilizes the custom Python tool
    print("[AGENT WORKFLOW] Calling extract_excel_grades tool...")
    tool_result = extract_excel_grades(file_path)
    
    if tool_result["status"] == "error":
        return f"Agent Error: Could not extract data. Reason: {tool_result['message']}"
        
    raw_data = tool_result["data"]
    
    # Step 2: The Agent reasons about the extracted data
    print("[AGENT WORKFLOW] Passing data to the local LLM for validation...\n")
    response = chain.invoke({"raw_data": str(raw_data)})
    
    return response.content

# --- Local Testing Block ---
if __name__ == "__main__":
    test_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_grades.xlsx")
    
    # Run the agent and print the AI's response
    final_output = run_ingestion_agent(test_file)
    print("=== AI AGENT FINAL OUTPUT ===")
    print(final_output)