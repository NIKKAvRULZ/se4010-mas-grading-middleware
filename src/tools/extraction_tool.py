import pandas as pd
from typing import List, Dict, Any
import os

def extract_grades(file_path: str) -> List[Dict[str, Any]]:
    """
    Extracts grading data from an Excel spreadsheet.
    Falls back to mock data if the file does not exist.
    """
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            return df.to_dict(orient='records')
        except Exception as e:
            print(f"Failed to read real Excel file: {e}")
            
    # Mock data fallback for demonstration
    return [
        {"student_id": "IT21000001", "name": "John Doe", "grade": 85},
        {"student_id": "IT21000002", "name": "Jane Smith", "grade": 92},
        {"student_id": "IT21000003", "name": "Alice Brown", "grade": 105}, # Anomaly
        {"student_id": "IT21000004", "name": "Bob White", "grade": -5}    # Anomaly
    ]
