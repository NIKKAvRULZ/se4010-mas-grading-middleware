import unittest
from src.tools.audit_tool import audit_grades

class TestGovernanceAgent(unittest.TestCase):
    def test_property_audit(self):
        mock_data = [
            {"student_id": "1", "grade": 85},
            {"student_id": "2", "grade": 105}, # Invalid
            {"student_id": "3", "grade": -5}   # Invalid
        ]
        
        valid, anomalies = audit_grades(mock_data)
        
        self.assertEqual(len(valid), 1)
        self.assertEqual(len(anomalies), 2)
        
if __name__ == "__main__":
    unittest.main()
