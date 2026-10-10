# Actuarial Risk & Predictive Analytics Pipeline: Pandemic Financial Solvency Framework
**Lead Analyst:** Lenny Wanjiru | *Dedan Kimathi University of Technology (DeKUT)*  
**Core Stack:** Python, SQLite, `scipy`, `lifelines`, `matplotlib`

---

##  Candidate Internship Profile & Value Proposition
This repository serves as a production-ready demonstration of advanced data engineering, epidemiological modeling, and non-parametric survival analysis. It transitions messy, unstructured insurance registers into highly optimized relational structures and executes stochastic simulations to deliver data-backed solvency recommendations for corporate portfolios.

---

##  Pipeline Architecture & Execution Roadmap
To audit or execute this framework, deploy the components sequentially within your environment to preserve database file dependencies and tracking variables:

1.  **`01_data_import.py`** *(Data Engineering & Relational Ingestion)*  
    Parses unstructured baseline csv data, executes schema normalizations, and serializes records into a local SQLite engine.
2.  **`02_pandemic_simulation.py`** *(Epidemiological Forecasting)*  
    Solves deterministic SEIR ordinary differential equations (ODE) to model sudden disease transmission velocities and projects daily macro liquidity outflows.
3.  **`03_survival_analysis.py`** *(Time-to-Event Operational Adjudication)*  
    Deploys non-parametric Kaplan-Meier estimators to track claim settlement lifespans and quantify pipeline processing bottlenecks.
4.  **`04_stochastic_monte_carlo.py`** *(Stochastic Solvency Simulation)*  
    Evolves the model into a 1,000-trial parallel Monte Carlo framework to isolate 95% Value at Risk (VaR) and Tail Value at Risk (TVaR) capital thresholds.

---

##  Core Engineering & Analytical Highlights

### Phase 1: Data Ingestion & Relational Architecture
*   **Execution:** Automates the extraction of raw records (`claim_data.csv`), programmatically enforcing uniform snake_case mapping across headers to neutralize formatting anomalies.
*   **Baseline Profile:** Relational database joins isolated distinct sector average billing metrics: Commercial (\$301.80), Medicaid (\$303.14), Medicare (\$283.71), and Self-Pay (\$299.41).

### Phase 2: Macro Epidemic Financial Shock Simulation
*   **Execution:** Integrates a deterministic SEIR differential calculus engine (β: 0.85, σ: 0.20, γ: 0.10) across a 120-day wave horizon.
*   **Actuarial Stress Result:** Factoring a 12% hospitalization constraint paired with a 2.5x medical severity loading index, the model successfully isolated an acute liquidity drain peaking at **\$142.5k on Day 34**, resulting in a cumulative **\$2,338,148.34** portfolio shock.

### Phase 3: Actuarial Survival Analysis & Processing Bottlenecks
*   **Execution:** Calculates non-parametric settlement probabilities to monitor claims duration from entry to final adjudication.
*   **Operational Diagnostic:** Revealed massive processing latency where **33.8% of active claims remain unresolved past Day 60**. Stratified tests proved Medicaid achieves the fastest turnaround (34-day median), outperforming commercial alternatives by 4 full days.

### Phase 4: Stochastic Loss Modeling & Extreme Tail Buffers
*   **Execution:** Runs a 1,000-run parameter shock model, drawing fluid transmission inputs via a Normal distribution and right-skewed severity loads via a Log-normal distribution.
*   **Solvency Output:** Expected mean loss settled at \$2,380,064.71, with a calculated **95% Value at Risk (VaR) of \$3,046,488.85** and a **95% Tail Value at Risk (TVaR) of \$3,239,669.43**.

---

##  Repository Tree Structure
```text
health_pandemic_cost/
├── data/
│   ├── claim_data.csv
│   ├── healthcare_risk.db
│   ├── claims_survival_processed.csv
│   ├── pandemic_financial_shock_forecast.csv
│   └── stochastic_monte_carlo_results.csv
├── scripts/
│   ├── 01_data_import.py
│   ├── 02_pandemic_simulation.py
│   ├── 03_survival_analysis.py
│   └── 04_stochastic_monte_carlo.py
├── documentation/
│   ├── project_methodology.md
│   └── kaplan_meier_curve.png
└── README.md
```

---

##  Quick Start Execution Guide
Ensure you have the required analytical libraries active in your workspace environment before running the modular scripts sequentially:

```bash
# Install core quantitative dependencies
pip install pandas numpy scipy lifelines matplotlib

# Execute the pipeline modules in order
python scripts/01_data_import.py
python scripts/02_pandemic_simulation.py
python scripts/03_survival_analysis.py
python scripts/04_stochastic_monte_carlo.py
```
