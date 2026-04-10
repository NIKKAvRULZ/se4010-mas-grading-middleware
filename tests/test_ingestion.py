import unittest
from src.tools.extraction_tool import extract_grades

class TestIngestionAgent(unittest.TestCase):
    def test_grade_extraction(self):
        # By default this will return the mock list of 4 students
        data = extract_grades("missing_file.xlsx")
        
        self.assertEqual(len(data), 4)
        
        # Verify schema includes student details
        self.assertIn("student_id", data[0])
        self.assertIn("name", data[0])
        self.assertIn("grade", data[0])
        
if __name__ == "__main__":
    unittest.main()
