# Actuarial Risk Analysis: Pandemic Financial Shock & Claims Reserving Framework

**Author:** Aspiring Actuarial Student & Data Analyst  
**Objective:** Model cash flow stress testing, financial loss propagation, and account settlement timelines within an insurance portfolio during an epidemic emergency.

---

##  1. Executive Summary
This project builds an integrated data engineering and risk forecasting pipeline to simulate the financial solvency impact of a sudden pandemic wave on a health insurance portfolio. By combining relational database mapping (SQL), epidemiological differential calculus (SEIR Model), and time-to-event risk forecasting (Kaplan-Meier Survival Analysis), we quantify precise balance sheet vulnerabilities.

###  Core Analytical Discoveries
 **Baseline Cost Loading:** The historical average payout baseline settles at **\$200.75 per claim**.
 **Total Pandemic Loss Impact:** The modeled pandemic surge creates an immediate **\$2,338,148.34 financial claim hit** to the fund.
 **Solvency Capital Cushion:** To avoid catastrophic insolvency under this stress test, the company must increase cash reserves by **+\$2,805,778.01 (representing a 120% margin buffer)**.
 **Cash Flow Processing Bottlenecks:** Actuarial censoring models prove that **33.8% of claims remain unresolved after 60 days**, causing severe systemic illiquidity.

---

##  2. Data Infrastructure & SQL Pipeline (`scripts/01_data_import.py`)
To keep the infrastructure portable, robust, and reproducible, raw billing data (`claim_data.csv`) is parsed programmatically using Python and mapped into a local **SQLite database** (`healthcare_risk.db`). 

### Data Cleaning Strategy
 Programmatic column trimming and whitespace character extraction.
 Capitalization mapping to convert headers into standardized database format (`billed_amount`, `paid_amount`, `claim_status`, `insurance_type`).

### Baseline Analytical Discoveries (SQL Output)
Our baseline engine grouped claims across individual insurance sectors to extract true financial exposure metrics before the pandemic surge:
 **Commercial Sector:** 259 total historical claims | Average billing of \$303.14.
 **Medicaid Sector:** 259 total historical claims | Average billing of \$301.80.
 **Medicare Sector:** 233 total historical claims | Average billing of \$283.71.
 **Self-Pay Sector:** 249 total historical claims | Average billing of \$299.41.

---

##  3. Epidemiological & Macro-Financial Forecasting (`scripts/02_pandemic_simulation.py`)
We implemented a system of ordinary differential equations (ODE) via `scipy.integrate.odeint` to evaluate disease transmission vectors across **100,000 insured individuals** over a 120-day horizon:

 **Transmission Metric (β):** 0.85
 **Incubation Period (σ):** 0.20 (5-day progression window)
 **Recovery Rate (γ):** 0.10 (10-day recovery timeline)
 **Severity Assumptions:** 12% hospitalization rate, with pandemic clinical interactions valued at a **2.5x severity load** multiplier relative to normal operating averages.

### Peak Outflow Dynamics
The simulation tracks an intense pressure wave beginning at Day 26 (\$25.6k/day) and accelerating rapidly to **peak liquidity drain on Day 34 (\$142.5k/day)**, which threatens standard working capital reserves.

---

##  4. Individual Micro-Risk Modeling (`scripts/03_survival_analysis.py`)
Using the `lifelines` engine, we constructed **Kaplan-Meier survival curves** tracking claim settlement cycle times from "Under Review" to ultimate resolution ("Paid" or "Denied").

### Processing Speed Stratification Matrix
 **Day 10 Pipeline Status:** 92.8% of claims are still stuck processing.
 **Day 30 Pipeline Status:** 54.7% of claims are still stuck processing.
 **Day 60+ Pipeline Horizon:** 33.8% clear floor threshold (Censored data tracking limitation).

### Median Operational Longevity Matrix
 **Medicaid:** 34.0 Days to full clearance cycle (Fastest settlement pathway).
 **Commercial / Medicare / Self-Pay:** 38.0 Days to final adjudication.
 ---

##  5. Stochastic Loss Modeling (Monte Carlo Engine) (`scripts/04_stochastic_monte_carlo.py`)
To account for tail risk and parameter uncertainty, we evolved our deterministic framework into a stochastic simulation environment by running **1,000 independent risk trials**:

 **Transmission Flux:** Modeled using a Normal Distribution (μ=0.85, σ=0.10) to capture random virus transmission variances.
 **Severity Shock Volatility:** Modeled using a Lognormal Distribution (μ=0.916, σ=0.15) to replicate severe right-skewed medical ICU billing spikes.

### Actuarial Tail Metrics Output
 **Expected (Mean) Portfolio Loss:** \$2,380,064.71
 **95% Value-at-Risk (VaR):** \$3,046,488.85 *(The maximum loss threshold with 95% confidence)*
 **95% Tail Value-at-Risk (TVaR / CVaR):** \$3,239,669.43 *(The average expected loss if the pandemic breaks into the catastrophic worst 5% tail)*

**Strategic Decision Matrix:** To ensure institutional solvency against 95% of all simulated volatile tail events, the corporate cash reserve cushion must be formally capped at **\$3,046,488.85**.
*