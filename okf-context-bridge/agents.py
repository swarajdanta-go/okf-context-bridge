from anthropic import AnthropicVertex
import os

# Initialize Claude via Google Cloud Vertex AI for enterprise security
# Requires Google Cloud credentials (e.g., gcloud auth application-default login)
client = AnthropicVertex(
    region="us-central1",
    project_id=os.environ.get("GOOGLE_CLOUD_PROJECT")
)

MODEL = "claude-3-5-sonnet@20240620"

def context_enricher_agent(table_name: str, raw_schema: str) -> dict:
    """
    Sub-Agent: Takes raw SQL and generates human-readable OKF context.
    Returns a dictionary containing the enriched description and column definitions.
    """
    prompt = f"""
    You are an expert Data Engineer. Analyze this raw SQL schema: {raw_schema}
    
    Deduce the business context. Translate cryptic names (e.g., 'usr_tbl' -> 'Users', 'vpa_id' -> 'Virtual Payment Address').
    
    Output strictly in this format:
    Description: <Overall business description of the table>
    Columns:
    - <col_name>: <Plain English description>
    """
    
    response = client.messages.create(
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
        model=MODEL,
    )
    
    # Simple parser for the agent's output
    text = response.content[0].text
    lines = text.split('\n')
    
    desc = next(line.split('Description: ')[1] for line in lines if line.startswith('Description:'))
    cols = [line.replace('- ', '') for line in lines if line.startswith('- ')]
    
    return {"description": desc, "columns": cols}
