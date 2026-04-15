import os
import sys
import json

# Add the root directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.agents.ingestion_agent import run_ingestion_agent
from src.tools.extraction_tool import extract_excel_grades

def test_ingestion_accuracy():
    """
    Automated test to ensure the LLM output matches the exact length of the raw data,
    proving no student records were hallucinated or dropped.
    """
    print("--- Running Automated Ingestion Test ---")
    test_file = os.path.join(os.path.dirname(__file__), "..", "data", "sample_grades.xlsx")
    
    # 1. Get the raw tool baseline
    baseline_result = extract_excel_grades(test_file)
    baseline_count = len(baseline_result["data"])
    
    # 2. Get the Agent's LLM output
    agent_output = run_ingestion_agent(test_file)
    
    # 3. Try to parse the agent's output as strict JSON
    try:
        parsed_output = json.loads(agent_output)
        
        # Access the "students" array we told the AI to create
        agent_records = parsed_output.get("students", [])
        agent_count = len(agent_records)
        
        # 4. Assertions
        assert agent_count == baseline_count, f"Data loss detected! Tool found {baseline_count}, Agent returned {agent_count}."
        print("\n✅ TEST PASSED: Agent successfully retained all student records without dropping data.")
        print("✅ TEST PASSED: Agent output is strictly valid JSON format.")
        
    except json.JSONDecodeError:
        print("\n❌ TEST FAILED: Agent hallucinated text and did not return strict JSON.")
        print(f"Agent Output was:\n{agent_output}")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")

if __name__ == "__main__":
    test_ingestion_accuracy()