from typing import List, Dict, Any, Tuple
import os
import json

def audit_grades(grades: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Checks for mathematical anomalies (e.g. grades > 100 or < 0).
    Separates valid grades from anomalies.
    """
    valid_grades = []
    anomalies = []
    
    for record in grades:
        grade = record.get("grade")
        if isinstance(grade, (int, float)) and (0 <= grade <= 100):
            valid_grades.append(record)
        else:
            anomalies.append(record)
            
    return valid_grades, anomalies

def write_audit_log(anomalies: List[Dict[str, Any]], output_dir: str = "data/outputs"):
    """
    Logs anomalies to a JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "audit_log.json")
    
    with open(file_path, "w") as f:
        json.dump(anomalies, f, indent=4)
