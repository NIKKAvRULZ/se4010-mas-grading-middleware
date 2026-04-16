from datetime import datetime
import json

def generate_audit_log(data: dict) -> str:
    """
    Save verified data into a file.

    Args:
        data (dict): student data

    Returns:
        str: file name
    """

    try:
        filename = f"audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        return filename

    except Exception as e:
        return f"Error: {str(e)}"