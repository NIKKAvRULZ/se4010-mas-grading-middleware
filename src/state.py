from typing import TypedDict, List, Dict, Any, Optional

class GradingBatchState(TypedDict):
    """
    The Global State dictionary passed between the 4 agents.
    This tracks the lifecycle of the grading data from raw file to blockchain payload.
    """
    # 1. Input
    file_path: str
    
    # 2. Nithika's Output (Ingestion)
    raw_json: Optional[List[Dict[str, Any]]]
    
    # 3. Dilki's Output (Governance/Audit)
    audit_status: Optional[str]
    audit_log_path: Optional[str]
    
    # 4. Susara's Output (Privacy/ZKP)
    anonymized_data: Optional[List[Dict[str, Any]]]
    
    # 5. Imesh's Output (Ledger Anchoring)
    merkle_root: Optional[str]
    
    # Global Error Tracking
    errors: Optional[List[str]]