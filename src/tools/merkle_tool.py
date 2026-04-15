def generate_merkle_root(data: list) -> str:
    """
    Generate a Merkle Root from a list of hashed records.

    Args:
        data (list): List of hashed strings.

    Returns:
        str: Merkle root hash.
    """

    if not data:
        return None

    import hashlib

    current_level = [hashlib.sha256(d.encode()).hexdigest() for d in data]

    while len(current_level) > 1:
        next_level = []

        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left

            combined = left + right
            new_hash = hashlib.sha256(combined.encode()).hexdigest()

            next_level.append(new_hash)

        current_level = next_level

    return current_level[0]