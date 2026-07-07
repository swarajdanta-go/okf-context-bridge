from mcp.server.fastmcp import FastMCP
import sqlite3

# Initialize the MCP Server
mcp = FastMCP("Fintech_DB_Server")

def get_connection():
    return sqlite3.connect('fintech.db')

@mcp.tool()
def list_tables() -> list[str]:
    """Returns a list of all tables in the database."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in c.fetchall()]
    conn.close()
    return tables

@mcp.tool()
def get_table_schema(table_name: str) -> str:
    """Returns the raw SQL schema (DDL) for a specific table."""
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    schema = c.fetchone()[0]
    conn.close()
    return schema

if __name__ == "__main__":
    # In a real environment, this runs on stdio or HTTP for the client to connect.
    mcp.run(transport='stdio')
