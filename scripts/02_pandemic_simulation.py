
Project: Health Pandemic Cost & Predictive Analytics Pipeline
Module: SEIR Epidemiological Modelling & Actuarial Financial Shock Projections
Analyst: Lenny Wanjiru (DeKUT Actuarial Science)


import os
import sqlite3
import logging
import numpy as np
import pandas as pd
from scipy.integrate import odeint

# Configure enterprise logger interface
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Path Space Definition (Relative Schema)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
db_path = os.path.join(DATA_DIR, 'healthcare_risk.db')

if not os.path.exists(db_path):
    logging.error(f"Execution Aborted: Source database missing at: {db_path}")
    raise FileNotFoundError("Please execute the initialization database ingestion script first.")

# PARAMETER INGESTION: HISTORICAL RECORD EXTRACTION via SQL

logging.info("Extracting portfolio cost baselines from relational database...")
conn = sqlite3.connect(db_path)

cost_query = "SELECT AVG(billed_amount) as avg_b, AVG(paid_amount) as avg_p FROM synthetic_claims;"
baseline_costs = pd.read_sql_query(cost_query, conn).iloc[0]
conn.close()

# Fallback allocation logic to ensure execution continuity
avg_historical_billed = baseline_costs['avg_b'] if pd.notnull(baseline_costs['avg_b']) else 350.00
avg_historical_paid = baseline_costs['avg_p'] if pd.notnull(baseline_costs['avg_p']) else 200.00


# EPIDEMIOLOGICAL STRUCTURE: THE SEIR DIFFERENTIAL CALCULUS ENGINE

logging.info("Initializing deterministic SEIR differential forecasting engine...")

# Population Compartment Parameters
N = 100000
Beta = 0.85      # Transmission velocity factor
Sigma = 0.20     # Latency/Incubation rate parameter
Gamma = 0.10     # Recovery parameter index

# Initial state variables
S0 = N - 10
E0 = 10
I0 = 0
R0 = 0
initial_state = [S0, E0, I0, R0]

# Time horizon configuration (120-day wave surge span)
days = 120
t = np.linspace(0, days, days)

def seir_deriv(state, t, N, beta, sigma, gamma):
    """Calculates instantaneous rates of change across health states."""
    S, E, I, R = state
    dSdt = -beta * S * I / N
    dEdt = (beta * S * I / N) - (sigma * E)
    dIdt = (sigma * E) - (gamma * I)
    dRdt = gamma * I
    return [dSdt, dEdt, dIdt, dRdt]

# Execute numerical integration across the timeline array
results = odeint(seir_deriv, initial_state, t, args=(N, Beta, Sigma, Gamma))
S, E, I, R = results.T


# FINANCIAL ACTUARIAL TRANSFORMATION: CASH CONFLUENCE MODELLING

logging.info("Executing financial risk adjustments over epidemiological projections...")

# Core underwriting modifiers
hospitalization_rate = 0.12
pandemic_severity_multiplier = 2.5

# Extract localized daily incident volumes from absolute incidence differentials
daily_infections = np.diff(I, prepend=0)
daily_infections[daily_infections < 0] = 0  # Eliminate mathematical noise floor variations

daily_claims_volume = daily_infections * hospitalization_rate
daily_financial_cost = daily_claims_volume * (avg_historical_paid * pandemic_severity_multiplier)

# Assemble structural reporting matrix
simulation_df = pd.DataFrame({
    'day': np.arange(1, days + 1),
    'susceptible_pool': S.astype(int),
    'exposed_pool': E.astype(int),
    'active_infections': I.astype(int),
    'projected_daily_claims': daily_claims_volume.astype(int),
    'projected_daily_payout_shock': np.round(daily_financial_cost, 2)
})

# Serialize forecasts to local repository files
output_csv = os.path.join(DATA_DIR, 'pandemic_financial_shock_forecast.csv')
simulation_df.to_csv(output_csv, index=False)
logging.info(f"Forecast timeline safely exported to repository destination: {output_csv}")


# FINANCIAL AUDITING TERMINAL REPORTING

total_shock_loss = simulation_df['projected_daily_payout_shock'].sum()
recommended_solvency_reserve = total_shock_loss * 1.20

print("\n" + "="*80)
print("FINANCIAL SHOCK SUMMARY REPORT: SURGE EXPOSURE ANCHORS")
print("="*80)
print("Peak Financial Shock Wave Analytics (Days 25 to 35 Snapshot):")
print(simulation_df.iloc[24:35].to_string(index=False))
print("-"*80)
print(f"Total Predicted Cumulative Portfolio Claims Payout:   ${total_shock_loss:,.2f}")
print(f"Recommended Minimum Solvency Capital Reserve (1.20x): ${recommended_solvency_reserve:,.2f}")
print("="*80 + "\n")
