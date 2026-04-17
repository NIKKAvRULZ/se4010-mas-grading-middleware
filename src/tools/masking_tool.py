import hashlib
from typing import List, Dict, Any

def mask_pii(student_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Takes a list of student records and anonymizes Personally Identifiable Information (PII) 
    like names and student IDs using cryptographic hashing (SHA-256).
    """
    anonymized_data = []
    
    for record in student_data:
        masked_record = record.copy()
        
        # Hash 'student_id' if it exists in the record
        if "student_id" in masked_record:
            hashed_id = hashlib.sha256(str(masked_record["student_id"]).encode()).hexdigest()
            masked_record["student_id"] = hashed_id
            
        # Hash 'name' if it exists in the record
        if "name" in masked_record:
            hashed_name = hashlib.sha256(str(masked_record["name"]).encode()).hexdigest()
            masked_record["name"] = hashed_name
            
        anonymized_data.append(masked_record)
        
    return anonymized_data
