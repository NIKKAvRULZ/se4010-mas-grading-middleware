from src.tools.merkle_tool import generate_merkle_root

def test_merkle_root_change():
    data1 = ["a", "b", "c"]
    data2 = ["a", "b", "X"]

    root1 = generate_merkle_root(data1)
    root2 = generate_merkle_root(data2)

    assert root1 != root2, "Merkle root should change when data changes"

    print("✅ Test Passed: Root changes correctly")

if __name__ == "__main__":
    test_merkle_root_change()