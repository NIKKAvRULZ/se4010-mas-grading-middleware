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
2.  **Governance Agent:** Audits the extracted grades for mathematical anomalies.
3.  **Privacy Agent:** Anonymizes student PII using cryptographic hashing.
4.  **Ledger Agent:** Anchors the anonymized batch into a simulated Merkle Root payload.

## ⚙️ Technical Constraints
* **Orchestrator:** LangGraph
* **LLM Engine:** Local execution via Ollama (Llama 3 8B / Phi-3)
* **Language:** Python 3.10+
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
   git clone [https://github.com/YourUsername/se4010-mas-grading-middleware.git](https://github.com/YourUsername/se4010-mas-grading-middleware.git)
   cd se4010-mas-grading-middleware
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   ---
## 📂 Project Structure

```
se4010-mas-grading-middleware/
├── .gitignore                  # Ignore pycache, venv, and local logs
├── requirements.txt            # List libraries: langgraph, langchain, pandas, openpyxl
├── README.md                   # Instructions on how to run the system
│
├── data/                       # Mock data storage
│   ├── sample_grades.xlsx      # The mock file Nithika's tool reads
│   └── outputs/                # Where Dilki's audit logs will be saved
│
├── src/                        # Core Application Code
│   ├── __init__.py
│   ├── state.py                # Defines the LangGraph 'GradingBatch' state dictionary
│   ├── graph.py                # The main LangGraph orchestrator (wires everything together)
│   │
│   ├── agents/                 # Each person's Langchain LLM & Prompt setup
│   │   ├── __init__.py
│   │   ├── ingestion_agent.py  # (Nithika)
│   │   ├── governance_agent.py # (Dilki)
│   │   ├── privacy_agent.py    # (Susara)
│   │   └── ledger_agent.py     # (Imesh)
│   │
│   └── tools/                  # Each person's Custom Python Tool
│       ├── __init__.py
│       ├── extraction_tool.py  # (Nithika) - pandas logic
│       ├── audit_tool.py       # (Dilki) - file writing logic
│       ├── masking_tool.py     # (Susara) - hashlib logic
│       └── merkle_tool.py      # (Imesh) - string concatenation logic
│
└── tests/                      # Each person's Evaluation Script
    ├── test_ingestion.py       # (Nithika) - LLM-as-a-judge script
    ├── test_governance.py      # (Dilki) - Property-based test
    ├── test_privacy.py         # (Susara) - Regex PII test
    └── test_ledger.py          # (Imesh) - Hash verification test
```

---
## 💻 Running the System
**To execute the multi-agent pipeline and observe the workflow:**
```bash
python src/graph.py
```

---
Note: Ensure Ollama is actively running in the background before executing the script to avoid connection errors.
