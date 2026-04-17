# Secure Academic Grading MAS Middleware

A locally hosted Multi-Agent System (MAS) built for the **SE4010-CTSE** module. This system simulates a secure, privacy-preserving data ingestion and verification pipeline for academic grades, designed to act as middleware for a blockchain-based ledger.

## 👥 Team Members & Responsibilities
* **Imeshi** - Ledger Anchoring Agent & Merkle Root Tool (Component 1)
* **Dilki** - Governance Audit Agent & Logging Tool (Component 2)
* **Nithika** - Data Ingestion Agent & Extraction Tool (Component 3)
* **Susara** - Privacy Validation Agent & ZKP Masking Tool (Component 4)

## 🏗️ System Architecture
The system utilizes **LangGraph** to orchestrate a sequential pipeline of 4 specialized AI agents. It runs entirely locally to ensure zero cloud costs and strict data privacy.
1.  **Ingestion Agent:** Extracts raw grading data from offline `.xlsx` spreadsheets.
2.  **Governance Agent:** Audits the extracted grades for mathematical anomalies and logs the results.
3.  **Privacy Agent:** Anonymizes student PII using cryptographic hashing.
4.  **Ledger Agent:** Anchors the anonymized batch into a simulated Merkle Root payload for ledger integration.

## ⚙️ Technical Constraints
* **Orchestrator:** LangGraph
* **LLM Engine:** Local execution via Ollama (Llama 3 8B / Phi-3)
* **Development Stack:** Python 3.10+, langchain-ollama, pandas, grandalf (for visualization)
* **Cloud Dependency:** None (100% Local Execution)

---

## 🚀 Prerequisites & Installation
Ensure you have Python installed, as well as [Ollama](https://ollama.com/) running on your local machine.

1. **Pull the required local models:**
   ```bash
   ollama run llama3:8b
   ollama run phi3
   ```
2. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/se4010-mas-grading-middleware.git
   cd se4010-mas-grading-middleware
   ```
3. **Install the required Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---
## 📂 Project Structure

```
se4010-mas-grading-middleware/
├── .gitignore                  # Ignore pycache, venv, and local logs
├── requirements.txt            # List libraries: langgraph, langchain, pandas, grandalf
├── README.md                   # Project documentation
├── test_ollama.py              # Script to verify local Ollama connectivity
├── audit_log_*.json            # Generated audit logs (output from governance agent)
│
├── data/                       # Mock data storage
│   ├── sample_grades.xlsx      # Input file for the ingestion pipeline
│   └── outputs/                # Folder for system-generated visual outputs
│       └── mas_architecture.png # Automatically generated agent workflow diagram
│
├── src/                        # Core Application Code
│   ├── state.py                # Defines the LangGraph 'GradingBatchState'
│   ├── graph.py                # Main orchestrator (builds and runs the MAS pipeline)
│   │
│   ├── agents/                 # Agent logic and LLM prompt setups
│   │   ├── ingestion_agent.py  # (Nithika) - Data extraction agent
│   │   ├── governance_agent.py # (Dilki) - Integrity verification agent
│   │   ├── privacy_agent.py    # (Susara) - PII masking agent
│   │   └── ledger_agent.py     # (Imeshi) - Cryptographic anchoring agent
│   │
│   └── tools/                  # Custom Python tools used by agents
│       ├── extraction_tool.py  # (Nithika) - Spreadsheet parsing logic
│       ├── audit_logger.py     # (Dilki) - File execution and logging logic
│       ├── masking_tool.py     # (Susara) - Cryptographic hashing logic
│       └── merkle_tool.py      # (Imeshi) - Merkle Proof generation logic
│
└── tests/                      # System evaluations
    ├── test_ingestion.py       # (Nithika) - Extraction accuracy tests
    ├── test_verification.py    # (Dilki) - Anomaly detection logic tests
    ├── test_privacy.py         # (Susara) - PII leakage prevention tests
    └── test_ledger.py          # (Imeshi) - Cryptographic audit tests
```

---
## 💻 Running the System

**To verify the LLM connection:**
```bash
python test_ollama.py
```

**To execute the full multi-agent pipeline:**
```bash
python src/graph.py
```

### 📊 Features Highlighted During Execution:
*   **Terminal Visualization:** The pipeline's logic is printed in ASCII format in the terminal during startup.
*   **Workflow Diagram:** A Mermaid-based PNG diagram (`mas_architecture.png`) is automatically saved in `data/outputs/` upon every run.
*   **Observability:** Strict logging is implemented to track every stage of the pipeline in real-time.

---
Note: Ensure Ollama is actively running in the background before executing the script to avoid connection errors.
