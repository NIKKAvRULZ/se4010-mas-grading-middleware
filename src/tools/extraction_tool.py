import pandas as pd
import os

def extract_excel_grades(file_path: str) -> dict:
    """
    Reads an offline academic grading spreadsheet and extracts the data securely.
    
    Args:
        file_path (str): The local system path to the .xlsx grading file.
        
    Returns:
        dict: A dictionary containing a status code and the parsed student records.
    """
    print(f"[TOOL EXECUTING] Attempting to read file: {file_path}")
    
    # Verify the file actually exists to prevent crashes
    if not os.path.exists(file_path):
        return {"status": "error", "message": f"File not found at {file_path}"}
        
    try:
        # Read the excel file using pandas
        df = pd.read_excel(file_path)
        
        # Clean the data: drop any completely empty rows
        df = df.dropna(how='all')
        
        # Convert the dataframe into a JSON-friendly dictionary list
        records = df.to_dict(orient="records")
        
        print(f"[TOOL SUCCESS] Extracted {len(records)} student records.")
        return {"status": "success", "data": records}
        
    except Exception as e:
        print(f"[TOOL FAILED] Error reading Excel file: {e}")
        return {"status": "error", "message": str(e)}

# --- Local Testing Block ---
# If you run this file directly, it will test the function.
if __name__ == "__main__":
    test_path = "../../data/sample_grades.xlsx"
    # Adjust path slightly for running directly from the tools folder
    actual_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_grades.xlsx")
    
    result = extract_excel_grades(actual_path)
    print("\nFinal Output:")
    print(result)