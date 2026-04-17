from src.agents.governance_agent import verify_grades

def test_valid():
    state = {
        "data": [
            {"student_id": "IT01", "grade": 80},
            {"student_id": "IT02", "grade": 60}
        ]
    }

    result = verify_grades(state)

    assert result["status"] == "success"


def test_invalid():
    state = {
        "data": [
            {"student_id": "IT01", "grade": 150}
        ]
    }

    result = verify_grades(state)

    assert result["status"] == "failed"


if __name__ == "__main__":
    test_valid()
    test_invalid()
    print("All tests passed ✅")