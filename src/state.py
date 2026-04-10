from typing import TypedDict, List, Dict, Any, Annotated
import operator

class GradingBatch(TypedDict):
    """
    The state dictionary that is passed between the LangGraph agents.
    """
    file_path: str
    grades: List[Dict[str, Any]]
    anomalies: List[Dict[str, Any]]
    privacy_status: str
    merkle_root: str
    logs: Annotated[List[str], operator.add]
