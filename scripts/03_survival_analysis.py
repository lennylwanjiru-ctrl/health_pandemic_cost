import os
import sqlite3
import pandas as pd
import numpy as np

# Try importing the actuarial lifelines package; fallback to standard math if not installed
try:
    from lifelines import KaplanMeierFitter
    LIFELINES_AVAILABLE = True
except ImportError:
    LIFELINES_AVAILABLE = False

# 1. Load Data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
db_path = os.path.join(DATA_DIR, 'healthcare_risk.db')

print("--- Step 1: Querying Claims Lifespans from Database ---")
conn = sqlite3.connect(db_path)

# Query claims timeline fields 
query = """
SELECT 
    claim_id,
    insurance_type,
    claim_status,
    billed_amount,
    date_of_service
FROM synthetic_claims;
"""
df = pd.read_sql_query(query, conn)
conn.close()

# 2. Engineering Actuarial 'Duration' and 'Event' Flags
# Since we lack explicit closure dates, we engineer realistic settlement timelines 
# based on claim status to simulate tracking claims over a 90-day cycle.
np.random.seed(42)
df['duration_days'] = np.where(
    df['claim_status'] == 'Paid', np.random.randint(5, 30, size=len(df)),
    np.where(df['claim_status'] == 'Denied', np.random.randint(15, 60, size=len(df)),
             np.random.randint(60, 90, size=len(df))) # Pending / Under Review
)

# Actuarial Censoring Flag: 1 if claim is closed (Paid/Denied), 0 if still open/censored (Under Review/Pending)
df['claim_resolved'] = np.where(df['claim_status'].isin(['Paid', 'Denied']), 1, 0)

print(f" Data processed successfully for {len(df):,} insurance claims.")
print("   - Resolved Claims (Events occurred):", len(df[df['claim_resolved'] == 1]))
print("   - Active / Censored Claims (Still under review):", len(df[df['claim_resolved'] == 0]))

# 3. Running the Kaplan-Meier Actuarial Estimator
print("\n--- Step 2: Running Kaplan-Meier Settlement Curve Analysis ---")

if LIFELINES_AVAILABLE:
    kmf = KaplanMeierFitter()
    
    # Calculate global claim survival rate (probability of remaining unpaid over time)
    kmf.fit(durations=df['duration_days'], event_observed=df['claim_resolved'])
    
    print("\n Actuarial Table: Probability of a Claim Remaining UNRESOLVED Over Time:")
    # Print specific milestone intervals (Day 10, 30, 60)
    milestones = [10, 30, 60, 80]
    for day in milestones:
        prob = kmf.survival_function_at_times(day).values[0]
        print(f"   - After Day {day}: {prob*100:.1f}% of claims are still stuck processing.")
        
    # Stratify by Insurance Provider Types
    print("\n Settlement Variations across Insurance Sectors (Median Days to Resolution):")
    for provider in df['insurance_type'].unique():
        mask = df['insurance_type'] == provider
        kmf.fit(durations=df.loc[mask, 'duration_days'], event_observed=df.loc[mask, 'claim_resolved'])
        median_wait = kmf.median_survival_time_
        print(f"   - {provider}: Median resolution lifespan is {median_wait} days.")
else:
    print("\n 'lifelines' library not installed. Computing standard empirical resolution metrics instead:")
    # Fallback clean metric presentation if lifelines isn't fully installed yet
    summary = df.groupby('insurance_type').agg(
        avg_processing_window=('duration_days', 'mean'),
        resolution_rate=('claim_resolved', 'mean')
    ).reset_index()
    for _, row in summary.iterrows():
        print(f"   - {row['insurance_type']}: Avg window {row['avg_processing_window']:.1f} days | {row['resolution_rate']*100:.1f}% final closure rate.")

# Save dataset with actuarial duration labels for dashboarding
df.to_csv(os.path.join(DATA_DIR, 'claims_survival_processed.csv'), index=False)
print("\n Formatted survival fields exported to 'data/claims_survival_processed.csv'")





import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    from lifelines import KaplanMeierFitter
    LIFELINES_AVAILABLE = True
except ImportError:
    LIFELINES_AVAILABLE = False

# 1. Load Data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DOC_DIR = os.path.join(BASE_DIR, 'documentation')
db_path = os.path.join(DATA_DIR, 'healthcare_risk.db')

print("--- Step 1: Querying Claims Lifespans from Database ---")
conn = sqlite3.connect(db_path)
query = "SELECT claim_id, insurance_type, claim_status, billed_amount FROM synthetic_claims;"
df = pd.read_sql_query(query, conn)
conn.close()

# 2. Engineering Actuarial 'Duration' and 'Event' Flags
np.random.seed(42)
df['duration_days'] = np.where(
    df['claim_status'] == 'Paid', np.random.randint(5, 30, size=len(df)),
    np.where(df['claim_status'] == 'Denied', np.random.randint(15, 60, size=len(df)),
             np.random.randint(60, 90, size=len(df)))
)
df['claim_resolved'] = np.where(df['claim_status'].isin(['Paid', 'Denied']), 1, 0)

print("\n--- Step 2: Running Kaplan-Meier Settlement Curve Analysis ---")

if LIFELINES_AVAILABLE:
    kmf = KaplanMeierFitter()
    
    # Setup the plot figure layout
    plt.figure(figsize=(10, 6))
    
    # Plot curves stratified by each Insurance Provider Type
    for provider in df['insurance_type'].unique():
        mask = df['insurance_type'] == provider
        kmf.fit(
            durations=df.loc[mask, 'duration_days'], 
            event_observed=df.loc[mask, 'claim_resolved'], 
            label=f"{provider} Claims"
        )
        kmf.plot_survival_function(ci_show=False, linewidth=2.5)
        
        median_wait = kmf.median_survival_time_
        print(f"   - {provider}: Median resolution lifespan is {median_wait} days.")
        
    # Style the Actuarial Graph professionally
    plt.title("Kaplan-Meier Claim Adjudication Lifespan Curve", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel("Days Since Claim Submission", fontsize=12)
    plt.ylabel("Probability of Claim Remaining Unresolved", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=10, loc="upper right")
    plt.ylim(0, 1.05)
    
    # Save the chart as an image in your documentation folder
    graph_path = os.path.join(DOC_DIR, 'kaplan_meier_curve.png')
    plt.savefig(graph_path, bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"\n SUCCESS! The Kaplan-Meier survival graph has been generated and saved to:")
    print(f"    {graph_path}")
else:
    print("\n 'lifelines' library error. Graphing requires the lifelines engine.")