# Actuarial Risk & Predictive Analytics Pipeline: Pandemic Financial Solvency Framework

##  Project Overview
This repository contains an end-to-end data analytics and actuarial forecasting pipeline designed to stress-test a health insurance claims portfolio against a severe epidemic emergency. 

The project bridges the gap between traditional actuarial science and modern predictive modeling by chaining structural database warehousing (SQL), demographic transmission differential equations (SEIR Epidemiology Model), and right-censored time-to-event tracking (Kaplan-Meier Survival Analysis).

---

##  Repository Architecture

```text
health_pandemic_cost/
├── data/
│   ├── claim_data.csv                       # Baseline raw input billing spreadsheet
│   ├── healthcare_risk.db                  # Staged SQLite relational database file
│   ├── pandemic_financial_shock_forecast.csv # Projected daily pandemic cash outflows
│   └── claims_survival_processed.csv       # Claims engineered with duration metrics
├── scripts/
│   ├── 01_data_import.py                   # SQL ingestion, cleaning, & data profiling
│   ├── 02_pandemic_simulation.py           # SEIR math integration & financial loading
│   └── 03_survival_analysis.py            # Kaplan-Meier time-to-settlement estimation
├── documentation/
│   └── project_methodology.md              # Executive summary and analytical methodology
└── README.md                               # Primary landing portfolio page
```

---

##  Execution & Pipeline Mechanics

### Phase 1: Data Ingestion & Relational Profiling (`scripts/01_data_import.py`)
 Programmatically creates a portable SQLite engine instance.
 Strips trailing whitespaces and lowercases messy headers to secure structural query constraints.
 Generates historical operational data frameworks stratified by insurance payer sectors.

### Phase 2: Macro Epidemiological Capital Stress Testing (`scripts/02_pandemic_simulation.py`)
 Solves multi-compartment ordinary differential equations over a 120-day outbreak horizon.
 Extracts historical baseline losses (approx. **\$200.75 per claim**) and runs a **2.5x severity multiplier shock** for pandemic ICU encounters.
 Identifies a catastrophic **\$2,338,148.34 payout hit**, providing data-justified evidence for a **+\$2,805,778.01 Solvency Capital Cushion (120% margin buffer)**.

### Phase 3: Operational Cash Flow Survival Modeling (`scripts/03_survival_analysis.py`)
 Resolves structural data right-censoring for open inventory items.
 Employs the `lifelines` engine to verify system performance thresholds.
 Highlights accounts receivable bottlenecks, proving **33.8% of claims remain frozen past 60 days**, and flags variance performance shifts (e.g., Medicaid resolving 4 days quicker than commercial alternatives).

---

##  Quick Start Guide

### System Requirements & Prerequisites
Ensure you have a standard Python installation ready. Run the dependency library loading command inside your terminal:
```bash
  install pandas numpy scipy lifelines streamlit
```

### Execution Order
Run the underlying modeling engines sequentially to regenerate the tracking assets:
```bash
python scripts/01_data_import.py
python scripts/02_pandemic_simulation.py
python scripts/03_survival_analysis.py
```