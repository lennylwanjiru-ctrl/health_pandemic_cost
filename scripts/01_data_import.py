"""
Project: Health Pandemic Cost & Predictive Analytics Pipeline
Module: Relational Database Ingestion & Baseline Actuarial Aggregation
Analyst: Lenny Wanjiru (DeKUT Actuarial Science)
"""
import os
import sqlite3
import logging
import pandas as pd

# Configure enterprise logger interface for execution tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Path Space Definition (Relative Schema)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

csv_filename = 'claim_data.csv'
csv_path = os.path.join(DATA_DIR, csv_filename)
db_path = os.path.join(DATA_DIR, 'healthcare_risk.db')

# 2. Workspace File System Verification
if not os.path.exists(csv_path):
    logging.error(f"Execution Aborted: Required exposure file missing at destination path: {csv_path}")
    raise FileNotFoundError(f"Please position target exposure file '{csv_filename}' inside directory: {DATA_DIR}")

# 3. Data Transformation & Database Materialization
logging.info("Initializing unstructured data ingestion pipeline...")
df = pd.read_csv(csv_path)

# Enforce clean database schema standards across source headers
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Connect to relational engine and serialize dataframe observations
conn = sqlite3.connect(db_path)
df.to_sql('synthetic_claims', conn, if_exists='replace', index=False)
logging.info(f"Relational table 'synthetic_claims' successfully materialized inside schema: {db_path}")


# ACTUARIAL BASELINE ANALYSIS: EXPOSURE AGGREGATION VIA SQL

logging.info("Executing baseline portfolio underwriting analytics...")

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

df_insurance_risk = pd.read_sql_query(insurance_risk_query, conn)

# Safe termination of connection parameters
conn.close()
logging.info("Database transaction session closed safely.")

# Terminal Telemetry Output Layout
print("\n" + "="*80)
print("ACTUARIAL EXPOSURE SUMMARY: FINANCIAL ANALYSIS BY PROFILE STATUS")
print("="*80)
print(df_insurance_risk.to_string(index=False))
print("="*80 + "\n")
    
