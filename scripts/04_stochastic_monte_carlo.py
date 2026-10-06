import os
import sqlite3
import numpy as np
import pandas as pd
from scipy.integrate import odeint

# 1. Paths & Database Ingestion
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
db_path = os.path.join(DATA_DIR, 'healthcare_risk.db')

print("--- Step 1: Loading Database Baselines for Stochastic Engine ---")
conn = sqlite3.connect(db_path)
cost_query = "SELECT AVG(paid_amount) as avg_p FROM synthetic_claims;"
avg_historical_paid = pd.read_sql_query(cost_query, conn).iloc[0]['avg_p'] or 200.75
conn.close()

print(f" Baseline Paid Claim loaded: ${avg_historical_paid:.2f}")

# 2. Configure Monte Carlo Dimensions
N_TRIALS = 1000   # Run 1,000 independent pandemic scenarios
POPULATION = 100000
DAYS = 120
t = np.linspace(0, DAYS, DAYS)
hospitalization_rate = 0.12

# SEIR ODE function
def seir_deriv(state, t, N, beta, sigma, gamma):
    S, E, I, R = state
    dSdt = -beta * S * I / N
    dEdt = (beta * S * I / N) - (sigma * E)
    dIdt = (sigma * E) - (gamma * I)
    dRdt = gamma * I
    return [dSdt, dEdt, dIdt, dRdt]

print(f"\n--- Step 2: Simulating {N_TRIALS} Stochastic Risk Trials ---")
np.random.seed(42)  # For reproducibility

# Draw 1,000 random variables for our actuarial risk distributions
beta_distributions = np.random.normal(loc=0.85, scale=0.10, size=N_TRIALS)   # Virus transmission uncertainty
severity_distributions = np.random.lognormal(mean=0.916, sigma=0.15, size=N_TRIALS) # Claims severity skewness (mean ~2.5x)

trial_total_losses = []

for i in range(N_TRIALS):
    beta_val = max(0.1, beta_distributions[i])  # Prevent negative transmission rates
    severity_mult = severity_distributions[i]
    
    # Standard SEIR parameters for this specific trial
    sigma = 0.20
    gamma = 0.10
    initial_state = [POPULATION - 10, 10, 0, 0]
    
    # Solve ODE for this specific scenario
    results = odeint(seir_deriv, initial_state, t, args=(POPULATION, beta_val, sigma, gamma))
    S, E, I, R = results.T
    
    # Extract total financial damages
    daily_infections = np.diff(I, prepend=0)
    daily_infections[daily_infections < 0] = 0
    total_claims = daily_infections.sum() * hospitalization_rate
    total_financial_loss = total_claims * (avg_historical_paid * severity_mult)
    
    trial_total_losses.append(total_financial_loss)

# 3. Compute Actuarial Loss Distribution Metrics
losses = np.array(trial_total_losses)
mean_loss = np.mean(losses)
median_loss = np.median(losses)

# Value at Risk (VaR) and Conditional Value at Risk (TVaR / CVaR)
var_95 = np.percentile(losses, 95)
cvar_95 = losses[losses >= var_95].mean()

# Organize results into a summary file
summary_df = pd.DataFrame({'trial_id': np.arange(1, N_TRIALS + 1), 'total_loss': losses})
summary_csv = os.path.join(DATA_DIR, 'stochastic_monte_carlo_results.csv')
summary_df.to_csv(summary_csv, index=False)

print(" Monte Carlo Simulation Complete!")
print(f" Distribution metrics saved to: {summary_csv}\n")

print(" ACTUARIAL STOCHASTIC LOSS SUMMARY REPORT:")
print(f"   - Expected (Mean) Portfolio Loss:      ${mean_loss:,.2f}")
print(f"   - Median Simulated Loss Scenario:     ${median_loss:,.2f}")
print(f"   - 95% Actuarial Value-at-Risk (VaR):   ${var_95:,.2f}")
print(f"   - 95% Tail Value-at-Risk (TVaR/CVaR):  ${cvar_95:,.2f}")
print("-" * 50)
print(f" Actionable Executive Decision Point:")
print(f"   To guarantee solvency against 95% of all simulated volatile tail events,")
print(f"   the corporate reserve requirement must be safely capped at: ${var_95:,.2f}")