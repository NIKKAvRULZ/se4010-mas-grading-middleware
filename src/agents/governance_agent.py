from src.tools.audit_logger import generate_audit_log

def verify_grades(state: dict) -> dict:
    data = state.get("data", [])

    invalid = []

    for record in data:
        grade = record.get("grade")

        if grade is None or grade < 0 or grade > 100:
            invalid.append(record)

    if invalid:
        return {
            "status": "failed",
            "invalid_records": invalid
        }

    file = generate_audit_log(data)

    return {
        "status": "success",
        "verified_data": data,
        "log_file": file
    }