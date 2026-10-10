
Project: Health Pandemic Cost & Predictive Analytics Pipeline
Module: Stochastic Monte Carlo Simulation & Extreme Tail Solvency Modeling
Analyst: Lenny Wanjiru (DeKUT Actuarial Science)

import os
import sqlite3
import logging
import numpy as np
import pandas as pd
from scipy.integrate import odeint

# Configure enterprise logger interface for execution tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 1. Path Space Definition (Relative Schema)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
db_path = os.path.join(DATA_DIR, 'healthcare_risk.db')

if not os.path.exists(db_path):
    logging.error(f"Execution Aborted: Required schema missing at: {db_path}")
    raise FileNotFoundError("Please execute the primary initialization database ingestion script first.")

# PARAMETER INGESTION: DATABASE COHORT EXTRACTION via SQL

logging.info("Querying historical baseline loss metrics for stochastic engine...")
conn = sqlite3.connect(db_path)

cost_query = "SELECT AVG(paid_amount) as avg_p FROM synthetic_claims;"
baseline_costs = pd.read_sql_query(cost_query, conn).iloc
conn.close()

# Fallback allocation to guarantee execution continuity
avg_historical_paid = baseline_costs['avg_p'] if pd.notnull(baseline_costs['avg_p']) else 200.75

# STOCHASTIC MONTE CARLO CONFIGURATION: THE SIMULATION LOOP

logging.info("Initializing multi-trial compound stochastic risk simulation...")

N_TRIALS = 1000
POPULATION = 100000
DAYS = 120
hospitalization_rate = 0.12
t = np.linspace(0, DAYS, DAYS)

# Initial epidemiological compartments
S0 = POPULATION - 10
E0 = 10
I0 = 0
R0 = 0
initial_state = [S0, E0, I0, R0]

def seir_deriv(state, t, N, beta, sigma, gamma):
    """Calculates instantaneous transmission rates across compartments."""
    S, E, I, R = state
    dSdt = -beta * S * I / N
    dEdt = (beta * S * I / N) - (sigma * E)
    dIdt = (sigma * E) - (gamma * I)
    dRdt = gamma * I
    return [dSdt, dEdt, dIdt, dRdt]

# Generate independent random variables to model systemic uncertainty boundaries
np.random.seed(42)
beta_distributions = np.random.normal(loc=0.85, scale=0.10, size=N_TRIALS)
severity_distributions = np.random.lognormal(mean=0.916, sigma=0.15, size=N_TRIALS)

trial_total_losses = []

# Execute parallel stochastic modeling loops
for i in range(N_TRIALS):
    # Enforce safe structural boundary constraints on virus transmission velocity
    beta_val = max(0.1, beta_distributions[i])
    severity_mult = severity_distributions[i]
    
    # Standard static structural parameters per specific iteration step
    sigma = 0.20
    gamma = 0.10
    
    # Solve SEIR system via ordinary differential equations
    results = odeint(seir_deriv, initial_state, t, args=(POPULATION, beta_val, sigma, gamma))
    S, E, I, R = results.T
    
    # Isolate daily incident differentials and drop negative mathematical noise
    daily_infections = np.diff(I, prepend=0)
    daily_infections[daily_infections < 0] = 0
    
    total_claims = daily_infections.sum() * hospitalization_rate
    total_financial_loss = total_claims * (avg_historical_paid * severity_mult)
    
    trial_total_losses.append(total_financial_loss)

# Convert arrays into structured numpy components for statistical aggregation
losses = np.array(trial_total_losses)
mean_loss = np.mean(losses)
median_loss = np.median(losses)


# CAPITAL ADEQUACY MATRIX: SOLVENCY CALCULATIONS

logging.info("Compiling solvency parameters across extreme simulation tails...")

var_95 = np.percentile(losses, 95)
cvar_95 = losses[losses >= var_95].mean()

# Organize results into an analytical data frame asset
summary_df = pd.DataFrame({
    'trial_id': np.arange(1, N_TRIALS + 1),
    'total_loss': losses
})

summary_csv = os.path.join(DATA_DIR, 'stochastic_monte_carlo_results.csv')
summary_df.to_csv(summary_csv, index=False)
logging.info(f"Stochastic outcome matrices safely written to destination: {summary_csv}")


# CORPORATE AUDITING TERMINAL REPORTING

print("\n" + "="*80)
print("ACTUARIAL STOCHASTIC LOSS SUMMARY REPORT: MONTE CARLO INFRASTRUCTURE")
print("="*80)
print(f"Expected (Mean) Portfolio Loss Scope:      ${mean_loss:,.2f}")
print(f"Median Simulated Loss Scenario Baseline:   ${median_loss:,.2f}")
print(f"95% Actuarial Value-at-Risk (VaR):         ${var_95:,.2f}")
print(f"95% Tail Value-at-Risk (TVaR / CVaR):      ${cvar_95:,.2f}")
print("-"*80)
print("Actionable Executive Decision Point:")
print(f"To guarantee solvency against 95% of simulated volatile tail events,")
print(f"the corporate reserve requirement must be safely capped at: ${var_95:,.2f}")
print("="*80 + "\n")
