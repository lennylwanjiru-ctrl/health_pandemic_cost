# Actuarial Risk Analysis: Pandemic Financial Shock & Claims Reserving Framework
**Lead Analyst:** Lenny Wanjiru | *Dedan Kimathi University of Technology (DeKUT)*  
**Infrastructure Specifications:** Python (100%), SQLite, `scipy`, `lifelines`, `matplotlib`



## 1. Executive Summary & Core Analytical Discoveries
This framework implements an end-to-end data science and actuarial forecasting pipeline to quantify the systemic macro-financial solvency impacts of sudden pandemic wave shocks on healthcare insurance portfolios. By linking deterministic compartmental epidemiology with non-parametric time-to-event claim survival curves and compound stochastic simulations, the pipeline converts raw case data into robust, risk-adjusted corporate cash reserves.

### Material Project Breakthroughs:
*   **Systemic Loss Footprint:** Macro stress-testing models demonstrate an immediate **\$2,338,148.34** aggregate claim hit to the insurance pool, indicating severe operational strain.
*   **Capital Adequacy Protection:** To mitigate the threat of catastrophic insolvency under peak stress conditions, the portfolio requires a **KES 2,805,778.01** capital cushion (reflecting an optimized 120% margin ceiling).
*   **Adjudication Bottlenecks:** Non-parametric survival curves prove that **33.8%** of active corporate claims remain stuck or unresolved in the processing pipeline beyond the 60-day operational margin, causing acute systemic illiquidity.



## 2. Relational Data Ingestion & SQL ETL Pipeline
*   **Component Driver:** `01_data_import.py`
*   **Infrastructure Strategy:** To ensure maximum deployment portability, reproducibility, and local data isolation, raw transactional file structures (`claim_data.csv`) are programmatically parsed, sanitized, and serialized directly into a decoupled local SQLite ecosystem (`healthcare_risk.db`).

### Operational Data Engineering Protocol:
1.  **Schema Normalization:** Executed string mutations, whitespace character trimmings, and capitalization mappings across raw source headers to build standard lowercase, snake_case table columns (`billed_amount`, `paid_amount`, `claim_status`, `insurance_type`).
2.  **Baseline Exploration:** Formulated core multi-table relational SQL query aggregates to isolate financial exposures by class prior to entering simulation loops. Initial baseline calculations confirmed an aggregate portfolio average billing baseline of **\$301.80** across the commercial line, **\$303.14** for Medicaid, **\$283.71** for Medicare, and **\$299.41** for Self-Pay accounts.



## 3. Epidemiological Forecasting & Macro-Financial Modeling
*   **Component Driver:** `02_pandemic_simulation.py`
*   **Methodology:** Deployed a deterministic system of ordinary differential equations (ODE) via `scipy.integrate.odeint` to track instantaneous population transitions across a standard 120-day pandemic wave horizon.

### Parametric Modeling Baselines:
*   **Transmission Velocity (β):** 0.85
*   **Incubation Rate (σ):** 0.20 (Translates to a 5-day progression window)
*   **Recovery Rate (γ):** 0.10 (Translates to a 10-day recovery cycle window)
*   **Initial Cohort Defenses:** Simulated a bounded environment of 100,000 insured individuals initiated with a starting infection index (I₀) of 10 active cases.
*   **Actuarial Risk Loadings:** Out-of-sample epidemiological case incidence differentials were mapped to underwriting liabilities by factoring a **12% systemic hospitalization rate** paired with an acute pandemic medical complexity cost multiplier of **2.5x** standard historical costs. 
*   **Liquidity Outflow Dynamics:** The pipeline isolated a severe financial pressure phase starting at Day 26 (\$25.6k daily payout velocity) accelerating rapidly to a peak portfolio liquidity drain on Day 34, tracking a maximum daily exposure run rate of **\$142.5k per day**.


## 4. Time-to-Event Survival Analysis & Adjudication Modeling
*   **Component Driver:** `03_survival_analysis.py`
*   **Methodology:** Utilized the `lifelines` engine to compute non-parametric Kaplan-Meier survival adjustments, tracking the exact settlement timelines and backlogs of processing claims from initial submission to final resolution ("Paid" or "Denied").

### Adjudication Lifespan Diagnostics:
*   **Processing Speeds:** Global lifetime estimations highlight severe timeline friction points. At Day 10 post-submission, **92.8%** of portfolio claims remain unresolved. This remains high at Day 30 (**54.7%** unresolved) and only drops to a **33.8%** clear floor threshold past Day 60, revealing critical backlogs.
*   **Stratified Provider Longevity Matrix (Median Days to Resolution):**
    *   *Medicaid:* **34.0 Days** to full clearance (Fastest operational settlement line).
    *   *Commercial / Medicare / Self-Pay:* **38.0 Days** to final adjudication.



## 5. Stochastic Loss Modeling & Solvency Analysis
*   **Component Driver:** `04_stochastic_monte_carlo.py`
*   **Methodology:** To fully account for parametric volatility and tail-risk uncertainty, the deterministic pipeline was evolved into a complex compound stochastic environment by executing a **1,000-trial parallel Monte Carlo simulation matrix**.

### Operational Parameter Shocks:
*   **Transmission Flux:** Modeled using a Normal Distribution (μ = 0.85, σ = 0.10) to capture random virus transmission variances.
*   **Severity Volatility:** Modeled using a log-normal distribution (μ = 0.916, σ = 0.15) to replicate severe right-skewed medical ICU billing spikes.

### Actuarial Tail Metrics Output:
*   **Expected (Mean) Portfolio Loss:** \$2,380,064.71
*   **95% Value at Risk (VaR):** **\$3,046,488.85** *(The maximum loss threshold expected with a 95% confidence boundary).*
*   **95% Tail Value at Risk (TVaR / CVaR):** **\$3,239,669.43** *(The expected conditional average loss if a catastrophic pandemic overshoot breaches the 95% tail boundary).*
*   **Capital Buffer Policy:** To guarantee total corporate solvency against 95% of all simulated extreme tail aggregations, the available cash reserves must be formally capped at **\$3,046,488.85**.
*
