# Patient Navigation Impact Analysis
### A Retrospective Propensity Score Matched Cohort Study

**Author:** Sai Manasa Adduru, MPH (Epidemiology), PharmD
**Methods:** Propensity Score Matching · Difference-in-Differences · Kaplan-Meier · Causal Inference

---

## 📋 Overview

This study evaluates whether structured **patient navigation** reduces post-discharge readmissions, emergency utilization, and healthcare cost — using the same analytical approaches applied in peer-reviewed health services research and health tech impact analytics.

---

## 🔑 Key Findings

| Outcome | Navigated | Control | Effect | p-value |
|---------|-----------|---------|--------|---------|
| 30-day readmission | **15.7%** | 24.0% | RR 0.65 · NNT 12.1 | 0.0007 |
| Adjusted OR (readmission) | — | — | **0.58** [0.43–0.79] | 0.0006 |
| 90-day ED visits | **0.64** | 0.80 | Δ −0.16 visits | 0.0020 |
| 180-day total cost | **$24,461** | $27,790 | **Savings $3,329/pt** | <0.0001 |

---

## 📊 Methods Summary

- **Cohort:** 2,000 patients (593 navigated, 1,407 usual care) following acute hospitalization
- **Matching:** 1:1 nearest-neighbor PSM, caliper = 0.02 SD → 555 matched pairs
- **Propensity model:** Logistic regression on 10 covariates (age, CCI, comorbidities, social risk) — c-statistic 0.71
- **Balance:** All 10 covariates achieved SMD <0.10 post-match
- **Causal methods:** Adjusted logistic regression, DiD cost analysis, log-rank test

---

## 📁 Repository Structure

```
├── data/
│   ├── simulate_cohort.py       # Synthetic claims-like data generator
│   └── synthetic_cohort.csv     # Generated cohort (2,000 patients)
├── analysis/
│   └── impact_analysis.py       # Full analysis: PSM, outcomes, figures
├── report/
│   ├── generate_report.py       # HTML report generator
│   └── impact_analysis_report.html   # Standalone research report
└── output/
    └── figures/                 # All publication-quality figures
```

---

## 🚀 Reproduce This Analysis

```bash
# 1. Clone and set up environment
git clone https://github.com/saimanasaadduru/patient-navigation-impact
cd patient-navigation-impact
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Generate data
python3 data/simulate_cohort.py

# 3. Run analysis
python3 analysis/impact_analysis.py

# 4. Build report
python3 report/generate_report.py
```

---

## 🛠 Tech Stack

`Python 3.9` · `pandas` · `scikit-learn` · `statsmodels` · `lifelines` · `matplotlib` · `seaborn`

---

## 📌 Why This Matters

Healthcare advocacy organizations need **rigorous, reproducible evidence** that their interventions improve outcomes and reduce cost. This analysis demonstrates how propensity score methods enable credible causal inference from observational claims data — the core methodology behind published outcomes research in health services and digital health.

---

*Synthetic data generated with NumPy for reproducibility. All patient identifiers are fabricated. Methods align with published guidance on propensity score analysis (Austin 2011, Rosenbaum & Rubin 1983).*
