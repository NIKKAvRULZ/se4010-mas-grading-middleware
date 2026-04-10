import unittest
from src.tools.merkle_tool import create_merkle_root

class TestLedgerAgent(unittest.TestCase):
    def test_merkle_generation(self):
        mock_masked_data = [
            {"student_id": "hash1", "name": "hash2", "grade": "A"}
        ]
        
        merkle_root = create_merkle_root(mock_masked_data)
        
        # Check that a 64 length SHA-256 hash string was correctly generated
        self.assertEqual(len(merkle_root), 64)
        
if __name__ == "__main__":
    unittest.main()
