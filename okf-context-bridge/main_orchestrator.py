import os
import yaml
from datetime import datetime
from agents import context_enricher_agent
# Note: In a full MCP implementation, we would use the MCP Client SDK to call the server.
# For this PoC orchestrator, we will simulate the tool responses for brevity.

def write_okf_concept(table_name: str, enriched_data: dict):
    """Writes the enriched data to disk adhering to the OKF v0.1 spec."""
    
    # 1. Build the mandatory YAML Frontmatter
    frontmatter = {
        "type": "Table",  # Required by OKF v0.1 specification
        "title": table_name,
        "description": enriched_data["description"],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    # 2. Build the Markdown Body
    md_body = f"# {table_name}\n\n"
    md_body += f"{enriched_data['description']}\n\n"
    md_body += "## Schema Details\n\n"
    for col in enriched_data["columns"]:
        md_body += f"* {col}\n"
        
    # 3. Combine and write to disk
    yaml_header = yaml.dump(frontmatter, sort_keys=False)
    final_content = f"---\n{yaml_header}---\n\n{md_body}"
    
    os.makedirs("okf_bundle/tables", exist_ok=True)
    file_path = f"okf_bundle/tables/{table_name}.md"
    
    with open(file_path, "w") as f:
        f.write(final_content)
    
    print(f"Generated OKF Concept: {file_path}")

def run_orchestrator():
    print("Starting OKF Pipeline...")
    
    # Step 1: MCP Tool Call - Get Tables (Simulated Client call)
    tables = ["usr_tbl", "txn_upi_log"] 
    
    for table in tables:
        # Step 2: MCP Tool Call - Get Schema (Simulated Client call)
        if table == "usr_tbl":
            raw_schema = "CREATE TABLE usr_tbl (usr_id TEXT PRIMARY KEY, kyc_stat TEXT)"
        else:
            raw_schema = "CREATE TABLE txn_upi_log (txn_id TEXT PRIMARY KEY, usr_id TEXT, vpa_id TEXT, amt REAL)"
            
        # Step 3: Sub-Agent Task - Enrich Context
        print(f"Enriching {table} via Claude on Vertex AI...")
        enriched_data = context_enricher_agent(table, raw_schema)
        
        # Step 4: Write OKF output
        write_okf_concept(table, enriched_data)

if __name__ == "__main__":
    run_orchestrator()
