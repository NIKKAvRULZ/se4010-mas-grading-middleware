from src.tools.merkle_tool import generate_merkle_root

def run_ledger_agent(hashed_records: list):
    """
    Ledger Anchoring Agent (Offline Mode)
    """

    print("🔗 Ledger Agent: Preparing data for blockchain...")
    print("📥 Input Records:", hashed_records)

    # Simulated reasoning (instead of Ollama)
    print("🤖 Simulated LLM: Deciding to generate Merkle Root...")

    # Call your tool
    merkle_root = generate_merkle_root(hashed_records)

    print("🌳 Merkle Root Generated:", merkle_root)

    return merkle_root


# Test run
if __name__ == "__main__":
    sample = ["a", "b", "c"]
    run_ledger_agent(sample)