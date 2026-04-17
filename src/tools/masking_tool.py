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
        
        # Updated to match Nithika's Excel columns
        if "CandidateID" in masked_record:
            hashed_id = hashlib.sha256(str(masked_record["CandidateID"]).encode()).hexdigest()
            masked_record["CandidateID"] = hashed_id
            
        if "First Name" in masked_record:
            hashed_first = hashlib.sha256(str(masked_record["First Name"]).encode()).hexdigest()
            masked_record["First Name"] = hashed_first
            
        if "Last Name" in masked_record:
            hashed_last = hashlib.sha256(str(masked_record["Last Name"]).encode()).hexdigest()
            masked_record["Last Name"] = hashed_last
            
        anonymized_data.append(masked_record)
        
    return anonymized_data