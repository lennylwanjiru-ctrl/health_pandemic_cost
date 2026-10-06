import os
import sqlite3
import pandas as pd

# 1. Define folder paths relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Set your Kaggle CSV filename to match your file exactly!
csv_filename = 'claim_data.csv' 
csv_path = os.path.join(DATA_DIR, csv_filename)
db_path = os.path.join(DATA_DIR, 'healthcare_risk.db')

print("--- Step 1: Loading data and creating database ---")

# 2. Check if the file exists
if not os.path.exists(csv_path):
    print(f" Error: Please move your downloaded Kaggle CSV file into the folder: {DATA_DIR}")
else:
    df = pd.read_csv(csv_path)
    
    # Clean column names (lowercase and underscores) so they work perfectly in SQL
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # 3. Create/Connect to local SQLite database
    conn = sqlite3.connect(db_path)
    
    # 4. Save dataframe as a SQL table
    df.to_sql('synthetic_claims', conn, if_exists='replace', index=False)
    print(f" Success! Created table 'synthetic_claims' inside: {db_path}\n")
    
    print("--- Step 2: Running Actuarial Baseline Queries via SQL ---")
    
    # 5. SQL Query: Financial Breakdown using your exact data columns
    insurance_risk_query = """
    SELECT 
        insurance_type,
        claim_status,
        COUNT(*) AS total_claims,
        ROUND(AVG(billed_amount), 2) AS avg_billed,
        ROUND(AVG(paid_amount), 2) AS avg_paid,
        ROUND(SUM(billed_amount) - SUM(paid_amount), 2) AS unpaid_financial_exposure
    FROM synthetic_claims
    GROUP BY insurance_type, claim_status
    ORDER BY insurance_type, total_claims DESC;
    """
    
    df_insurance_risk = pd.read_sql_query(insurance_risk_query, conn)
    print("\n Actuarial Baseline: Financial Breakdown by Status & Insurance Type:")
    print(df_insurance_risk.to_string(index=False))
    
    conn.close()