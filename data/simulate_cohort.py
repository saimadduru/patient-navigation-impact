"""
Synthetic Retrospective Cohort Data Generator
Simulates a claims-like dataset of patients discharged from hospital,
some of whom received patient navigation services post-discharge.
"""

import numpy as np
import pandas as pd

np.random.seed(42)
N = 2000

def generate_cohort(n=N):
    age = np.random.normal(65, 12, n).clip(30, 90).astype(int)
    female = np.random.binomial(1, 0.52, n)
    cci = np.random.poisson(2.1, n).clip(0, 8)          # Charlson Comorbidity Index
    prior_admits = np.random.poisson(1.4, n).clip(0, 6)
    index_los = np.random.poisson(4.2, n).clip(1, 20)   # Length of stay at index admission
    dual_eligible = np.random.binomial(1, 0.28, n)       # Medicare + Medicaid
    chf = np.random.binomial(1, 0.31, n)
    copd = np.random.binomial(1, 0.26, n)
    diabetes = np.random.binomial(1, 0.38, n)
    rural = np.random.binomial(1, 0.22, n)

    # Propensity to receive navigation: higher for complex/high-risk patients
    nav_logit = (
        -1.2
        + 0.025 * (age - 65)
        + 0.4  * chf
        + 0.3  * copd
        + 0.25 * (cci > 3).astype(int)
        + 0.35 * dual_eligible
        + 0.2  * (prior_admits > 2).astype(int)
        - 0.3  * rural
        + np.random.normal(0, 0.5, n)
    )
    nav_prob = 1 / (1 + np.exp(-nav_logit))
    navigated = np.random.binomial(1, nav_prob, n)

    # Outcomes — navigation reduces risk
    readmit_logit = (
        -1.8
        + 0.022 * (age - 65)
        + 0.5  * chf
        + 0.45 * copd
        + 0.3  * (cci > 3).astype(int)
        + 0.4  * (prior_admits > 2).astype(int)
        + 0.3  * dual_eligible
        - 0.55 * navigated              # navigation effect
        + np.random.normal(0, 0.4, n)
    )
    readmit_30 = np.random.binomial(1, 1 / (1 + np.exp(-readmit_logit)), n)

    er_visits_logit = (
        -0.9
        + 0.018 * (age - 65)
        + 0.35 * chf
        + 0.4  * copd
        + 0.3  * dual_eligible
        - 0.4  * navigated
        + np.random.normal(0, 0.4, n)
    )
    er_visits_90 = np.random.poisson(np.exp(er_visits_logit * 0.5).clip(0.1, 3), n)

    base_cost = (
        8000
        + 150  * age
        + 2500 * chf
        + 2000 * copd
        + 1800 * diabetes
        + 1200 * cci
        + 3500 * prior_admits
        - 3200 * navigated              # navigation reduces downstream cost
        + np.random.normal(0, 4000, n)
    ).clip(500, 80000)

    # Time to readmission (days), censored at 30 for non-events
    days_to_readmit = np.where(
        readmit_30 == 1,
        np.random.gamma(shape=2.5, scale=5, size=n).clip(1, 30).astype(int),
        30
    )
    event_observed = readmit_30.copy()

    df = pd.DataFrame({
        "patient_id":       [f"PT{str(i).zfill(5)}" for i in range(n)],
        "age":              age,
        "female":           female,
        "cci":              cci,
        "prior_admits_12m": prior_admits,
        "index_los":        index_los,
        "dual_eligible":    dual_eligible,
        "chf":              chf,
        "copd":             copd,
        "diabetes":         diabetes,
        "rural":            rural,
        "navigated":        navigated,
        "readmit_30d":      readmit_30,
        "er_visits_90d":    er_visits_90,
        "total_cost_180d":  base_cost.astype(int),
        "days_to_readmit":  days_to_readmit,
        "event_observed":   event_observed,
    })

    return df


if __name__ == "__main__":
    df = generate_cohort()
    df.to_csv("data/synthetic_cohort.csv", index=False)
    print(f"Generated {len(df)} patients  |  Navigated: {df.navigated.sum()}  |  Control: {(1-df.navigated).sum()}")
    print(f"Overall 30d readmit rate: {df.readmit_30d.mean():.1%}")
    print(f"Navigated 30d readmit:    {df[df.navigated==1].readmit_30d.mean():.1%}")
    print(f"Control 30d readmit:      {df[df.navigated==0].readmit_30d.mean():.1%}")
