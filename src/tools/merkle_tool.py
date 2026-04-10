import hashlib
import json
from typing import List, Dict, Any

def create_merkle_root(grades: List[Dict[str, Any]]) -> str:
    """
    Takes a list of privacy-masked grading records, sorts them for consistency,
    generates a hash for each, and then hashes the concatenation of all hashes
    to simulate a Blockchain Merkle Root for ledger anchoring.
    """
    if not grades:
        return ""
        
    # Serialize records to JSON strings and hash them
    hashed_records = []
    for record in grades:
        record_str = json.dumps(record, sort_keys=True).encode()
        record_hash = hashlib.sha256(record_str).hexdigest()
        hashed_records.append(record_hash)
        
    # Sort hashes for deterministic root generation
    hashed_records.sort()
    
    # Hash the concatenated hashes to construct a pseudo-Merkle Root
    concatenated = "".join(hashed_records).encode()
    merkle_root = hashlib.sha256(concatenated).hexdigest()
    
    return merkle_root
