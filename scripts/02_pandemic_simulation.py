import os
import sqlite3
import numpy as np
import pandas as pd
from scipy.integrate import odeint

# 1. Establish paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
db_path = os.path.join(DATA_DIR, 'healthcare_risk.db')

print("--- Step 1: Fetching Actuarial Cost Baselines from SQL ---")
conn = sqlite3.connect(db_path)

# Extract baseline values dynamically from your newly created database
cost_query = "SELECT AVG(billed_amount) as avg_b, AVG(paid_amount) as avg_p FROM synthetic_claims;"
baseline_costs = pd.read_sql_query(cost_query, conn).iloc[0]
avg_historical_billed = baseline_costs['avg_b'] or 350.00  # Fallback if empty
avg_historical_paid = baseline_costs['avg_p'] or 200.00    # Fallback if empty
conn.close()

print(f"📊 Historical Baseline Claims Parameters Loaded:")
print(f"   - Average Billed Amount per claim: ${avg_historical_billed:.2f}")
print(f"   - Average Paid Amount per claim: ${avg_historical_paid:.2f}\n")

print("--- Step 2: Running SEIR Epidemic Differential Equation Model ---")

# 2. SEIR Model Parameters
N = 100000        # Total insured population pool
Beta = 0.85       # Transmission rate (how fast it spreads)
Sigma = 0.20      # Incubation rate (moving from Exposed to Infected)
Gamma = 0.10      # Recovery rate (1/days until infectious period ends)

# Initial conditions: 10 exposed individuals, 0 infected, 0 recovered
S0 = N - 10
E0 = 10
I0 = 0
R0 = 0
initial_state = [S0, E0, I0, R0]

# Timeline: 120 days of the pandemic wave
days = 120
t = np.linspace(0, days, days)

# The SEIR Differential Equations framework
def seir_deriv(state, t, N, beta, sigma, gamma):
    S, E, I, R = state
    dSdt = -beta * S * I / N
    dEdt = (beta * S * I / N) - (sigma * E)
    dIdt = (sigma * E) - (gamma * I)
    dRdt = gamma * I
    return [dSdt, dEdt, dIdt, dRdt]

# Integrate equations over the timeline
results = odeint(seir_deriv, initial_state, t, args=(N, Beta, Sigma, Gamma))
S, E, I, R = results.T

# 3. Translate Epidemic Wave into Actuarial Financial Shock
# Let's assume 12% of infected individuals require standard medical treatment encounters
hospitalization_rate = 0.12
# Pandemic care costs 2.5 times more than standard historical baseline visits
pandemic_severity_multiplier = 2.5 

daily_infections = np.diff(I, prepend=0)
daily_infections[daily_infections < 0] = 0 # Clean numerical noise

daily_claims_volume = daily_infections * hospitalization_rate
daily_financial_cost = daily_claims_volume * (avg_historical_paid * pandemic_severity_multiplier)

# Build out the final output dataset table
simulation_df = pd.DataFrame({
    'day': np.arange(1, days + 1),
    'susceptible_pool': S.astype(int),
    'exposed_pool': E.astype(int),
    'active_infections': I.astype(int),
    'projected_daily_claims': daily_claims_volume.astype(int),
    'projected_daily_payout_shock': np.round(daily_financial_cost, 2)
})

# Save results down to data directory so the panel can view or audit them
output_csv = os.path.join(DATA_DIR, 'pandemic_financial_shock_forecast.csv')
simulation_df.to_csv(output_csv, index=False)

print("✅ Epidemic Simulation Complete!")
print(f"💾 Forecasted timeline exported to: {output_csv}\n")

print("📊 Peak Financial Shock Analysis (Days 25 to 35 Snapshot):")
print(simulation_df.iloc[25:35].to_string(index=False))

total_shock_loss = simulation_df['projected_daily_payout_shock'].sum()
print(f"\n🚨 CATASTROPHIC RISK SUMMARY FOR EXECUTIVE PANEL:")
print(f"   - Predicted Total Pandemic Claims Payout: ${total_shock_loss:,.2f}")
print(f"   - Recommended Minimum Solvency Capital Reserve Adjustments: +${(total_shock_loss * 1.2):,.2f}")