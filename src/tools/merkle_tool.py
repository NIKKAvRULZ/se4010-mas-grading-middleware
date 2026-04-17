import hashlib
import json

def generate_merkle_root(data: list) -> str:
    """
    Generate a Merkle Root from a list of hashed records.

    Args:
        data (list): List of student record dictionaries.

    Returns:
        str: Merkle root hash.
    """

    if not data:
        return None

    # FIX: Convert dictionaries to sorted JSON strings so they can be securely encoded
    stringified_data = [json.dumps(d, sort_keys=True) for d in data]
    
    # Hash the stringified records for the bottom layer of the Merkle Tree
    current_level = [hashlib.sha256(string_record.encode()).hexdigest() for string_record in stringified_data]

    while len(current_level) > 1:
        next_level = []

        for i in range(0, len(current_level), 2):
            left = current_level[i]
            # If there's an odd number of leaves, duplicate the last one (Standard Merkle logic)
            right = current_level[i + 1] if i + 1 < len(current_level) else left

            combined = left + right
            new_hash = hashlib.sha256(combined.encode()).hexdigest()

            next_level.append(new_hash)

        current_level = next_level

    return current_level[0]