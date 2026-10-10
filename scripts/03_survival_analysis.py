
Project: Health Pandemic Cost & Predictive Analytics Pipeline
Module: Actuarial Survival Analysis & Claim Adjudication Dwell-Time Modeling
Analyst: Lenny Wanjiru (DeKUT Actuarial Science)


import os
import sqlite3
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configure enterprise logger interface
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global execution safety guard for the lifelines statistical package
try:
    from lifelines import KaplanMeierFitter
    LIFELINES_AVAILABLE = True
except ImportError:
    logging.warning("The 'lifelines' library is missing from current environment. Visualization tracks will be bypassed.")
    LIFELINES_AVAILABLE = False

# 1. Path Space Definition (Relative Schema)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOC_DIR = os.path.join(BASE_DIR, 'documentation')
db_path = os.path.join(DATA_DIR, 'healthcare_risk.db')

if not os.path.exists(db_path):
    logging.error(f"Execution Aborted: Relational schema database missing at: {db_path}")
    raise FileNotFoundError("Please execute the primary initialization ingestion script first.")

# DATA INGESTION: EXTRACT LIFESPAN RECORDS FROM SQL

logging.info("Querying clinical claim adjudication timelines from database...")
conn = sqlite3.connect(db_path)

claims_query = "SELECT claim_id, insurance_type, claim_status, billed_amount FROM synthetic_claims;"
df = pd.read_sql_query(claims_query, conn)
conn.close()


# FEATURE ENGINEERING: ACTUARIAL TIMELINE & CENSORED FLAGS

logging.info("Engineering survival duration indices and censoring flags...")
np.random.seed(42)

# Simulate processing durations across outcome classes to model claim backlogs
df['duration_days'] = np.where(
    df['claim_status'] == 'Paid', np.random.randint(5, 30, size=len(df)),
    np.where(df['claim_status'] == 'Denied', np.random.randint(15, 60, size=len(df)),
             np.random.randint(60, 90, size=len(df)))
)

# Censoring Flag: 1 = Event Observed (Adjudicated), 0 = Right-Censored (Pending)
df['claim_resolved'] = np.where(df['claim_status'].isin(['Paid', 'Denied']), 1, 0)

total_records = len(df)
resolved_events = df['claim_resolved'].sum()
censored_events = total_records - resolved_events

logging.info(f"Cohort Parsing Complete. Total: {total_records} | Resolved: {resolved_events} | Pending/Censored: {censored_events}")


# SURVIVAL INFERENCE: THE KAPLAN-MEIER ADJUDICATION ESTIMATOR

if LIFELINES_AVAILABLE:
    logging.info("Deploying non-parametric Kaplan-Meier survival adjustments...")
    kmf = KaplanMeierFitter()
    
    # 1. Global Portfolio Survival Estimation
    kmf.fit(durations=df['duration_days'], event_observed=df['claim_resolved'])
    
    print("\n" + "="*80)
    print("ACTUARIAL LIFE TABLE: CLAIM UNRESOLVED PROBABILITY MILESTONES")
    print("="*80)
    milestones = [10, 30, 60, 80]
    for day in milestones:
        prob = kmf.survival_function_at_times(day).values[0]
        print(f"Time Horizon: Day {day:02d} | Probability of Claim Remaining Unpaid: {prob:.2%}")
    print("-"*80)

    # 2. Stratified Analysis & Visualization Across Industry Sector Risk Classes
    logging.info("Generating stratified survival functions by provider tier...")
    plt.figure(figsize=(10, 6))
    
    unique_providers = df['insurance_type'].unique()
    
    print("Stratified Adjudication Metrics:")
    for provider in unique_providers:
        mask = df['insurance_type'] == provider
        kmf.fit(durations=df.loc[mask, 'duration_days'], 
                event_observed=df.loc[mask, 'claim_resolved'], 
                label=f"{provider} Track")
        
        # Extract median survival duration bounds
        median_wait = kmf.median_survival_time_
        print(f" -> Provider Category [{provider}]: Median Resolution Lifespan = {median_wait:.1f} Days")
        
        # Plot corresponding parametric curve properties
        kmf.plot_survival_function(ci_show=False, linewidth=2.5)
        
    # Style and format the final corporate analytics chart
    plt.title("Kaplan-Meier Claim Adjudication Lifespan Curve", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Days Since Claim Submission", fontsize=12)
    plt.ylabel("Probability of Claim Remaining Unresolved", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10, loc="upper right")
    plt.ylim(0, 1.05)
    
    # Export material chart assets directly to documentation channels
    os.makedirs(DOC_DIR, exist_ok=True)
    graph_path = os.path.join(DOC_DIR, 'kaplan_meier_curve.png')
    plt.savefig(graph_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    logging.info(f"Production visualization asset safely materialized at target: {graph_path}")
    print("="*80 + "\n")

else:
    # Reliable fallback data engine if the lifelines module drops out of system paths
    logging.info("Executing empirical framework fallback metrics calculations...")
    summary = df.groupby('insurance_type').agg(
        avg_processing_window=('duration_days', 'mean'),
        resolution_rate=('claim_resolved', 'mean')
    ).reset_index()
    
    print("\n" + "="*80)
    print("FALLBACK AGGREGATION REPORT: RESOLUTION METRICS BY TIER")
    print("="*80)
    print(summary.to_string(index=False))
    print("="*80 + "\n")

# Export structured transformations for cross-module database storage
processed_csv = os.path.join(DATA_DIR, 'claims_survival_processed.csv')
df.to_csv(processed_csv, index=False)
logging.info(f"Processed analytical dataset successfully written to destination: {processed_csv}")
