# OKF Context Bridge

An enterprise-grade pipeline for automatically generating Open Knowledge Format (OKF) v0.1 bundles from raw database schemas.

This project bridges the "context gap" for AI agents by using **Claude on Google Cloud Vertex AI** to deduce business logic and the **Model Context Protocol (MCP)** to securely expose data infrastructure.

## Why This Exists

AI agents struggle to write accurate SQL or perform data analysis without understanding the underlying business context (e.g., knowing that `vpa_id` means "Virtual Payment Address").

Google Cloud introduced the **Open Knowledge Format (OKF)** to standardise how this context is delivered to agents via structured Markdown files. However, manually writing OKF files for thousands of database tables is not scalable.

The **OKF Context Bridge** automates this process. It acts as an "enrichment agent" that reads raw SQL schemas, deduces the business context using LLMs, and outputs strict OKF-compliant Markdown bundles ready for your AI agents to ingest.

## Architecture

This project implements advanced AI engineering patterns:

1.  **Model Context Protocol (MCP):** Secures the database connection. The database is exposed as standardized "tools" rather than hardcoding connection strings into the agent.
2.  **Claude on Vertex AI:** Keeps proprietary schema data secure within your Google Cloud boundary.
3.  **Sub-Agent Pattern:** Separates the orchestration logic from the context enrichment tasks.

## Prerequisites

*   Python 3.10+
*   Google Cloud Account with Vertex AI enabled
*   `gcloud` CLI installed and authenticated

## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/okf-context-bridge.git](https://github.com/yourusername/okf-context-bridge.git)
    cd okf-context-bridge
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4.  Authenticate with Google Cloud:
    ```bash
    gcloud auth application-default login
    ```

## Usage

1.  **Generate the Mock Database:**
    Creates a local `fintech.db` SQLite database with messy, undocumented tables to test the pipeline.
    ```bash
    python mock_db_setup.py
    ```

2.  **Run the Pipeline:**
    Executes the orchestrator, connects via MCP, enriches the schema using Claude, and generates the OKF bundle.
    ```bash
    python main_orchestrator.py
    ```

3.  **Inspect the Output:**
    Check the newly created `okf_bundle/tables/` directory. You will find `.md` files containing the LLM-enriched business context, formatted precisely to the OKF v0.1 specification.

## License
MIT License
