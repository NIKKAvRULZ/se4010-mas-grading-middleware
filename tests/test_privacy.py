import unittest
import re
from src.tools.masking_tool import mask_pii

class TestPrivacyAgent(unittest.TestCase):
    def test_pii_masking(self):
        # Mock data representing what the Governance Agent would output
        mock_data = [
            {"student_id": "IT21000001", "name": "John Doe", "grade": "A"},
            {"student_id": "IT21000002", "name": "Jane Smith", "grade": "B"}
        ]
        
        # Run the masking tool
        anonymized = mask_pii(mock_data)
        
        # Regex to ensure raw student ID format (IT + digits) is completely removed
        raw_id_pattern = re.compile(r"IT\d{8}")
        
        for record in anonymized:
            # 1. Check length of the hashed ID (SHA-256 produces 64 hex characters)
            self.assertEqual(len(record["student_id"]), 64)
            self.assertEqual(len(record["name"]), 64)
            
            # 2. Ensure raw IT number is gone from the student_id field
            self.assertFalse(raw_id_pattern.search(record["student_id"]))
            
            # 3. Ensure the grade remains intact (since it shouldn't be masked)
            self.assertIn(record["grade"], ["A", "B", "C", "D", "F"])

if __name__ == "__main__":
    unittest.main()
