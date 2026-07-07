import sqlite3

def setup_db():
    conn = sqlite3.connect('fintech.db')
    c = conn.cursor()
    # Create messy, undocumented tables
    c.execute('''CREATE TABLE usr_tbl (usr_id TEXT PRIMARY KEY, kyc_stat TEXT)''')
    c.execute('''CREATE TABLE txn_upi_log (txn_id TEXT PRIMARY KEY, usr_id TEXT, vpa_id TEXT, amt REAL)''')
    conn.commit()
    conn.close()
    print("Mock database 'fintech.db' created.")

if __name__ == "__main__":
    setup_db()
