"""
Runs all SQL cohort queries against the SQLite claims database.
Mirrors the SQL-first workflow used in Snowflake / BigQuery environments.
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect("data/claims.db")

queries = {
    "1. Cohort Overview": """
        SELECT COUNT(*) AS total_patients,
               SUM(n.navigated) AS navigated,
               COUNT(*) - SUM(n.navigated) AS control,
               ROUND(AVG(n.navigated)*100,1) AS pct_navigated
        FROM navigation_enrollment n
    """,
    "2. Baseline Characteristics by Navigation Status": """
        SELECT n.navigated, COUNT(*) AS n,
               ROUND(AVG(p.age),1) AS mean_age,
               ROUND(AVG(p.female)*100,1) AS pct_female,
               ROUND(AVG(p.dual_eligible)*100,1) AS pct_dual_eligible,
               ROUND(AVG(d.cci),2) AS mean_cci,
               ROUND(AVG(d.chf)*100,1) AS pct_chf,
               ROUND(AVG(d.copd)*100,1) AS pct_copd,
               ROUND(AVG(u.prior_admits_12m),2) AS mean_prior_admits
        FROM navigation_enrollment n
        JOIN patient_encounters p ON p.patient_id = n.patient_id
        JOIN diagnoses d ON d.patient_id = n.patient_id
        JOIN utilization u ON u.patient_id = n.patient_id
        GROUP BY n.navigated ORDER BY n.navigated
    """,
    "3. Primary Outcomes by Navigation Status": """
        SELECT n.navigated, COUNT(*) AS n,
               ROUND(AVG(u.readmit_30d)*100,1) AS readmit_rate_pct,
               ROUND(AVG(u.er_visits_90d),2) AS mean_er_visits_90d,
               ROUND(AVG(u.total_cost_180d),0) AS mean_cost_180d
        FROM navigation_enrollment n
        JOIN utilization u ON u.patient_id = n.patient_id
        GROUP BY n.navigated ORDER BY n.navigated
    """,
    "4. High-Risk Subgroup (Dual Eligible + CCI >= 3)": """
        SELECT n.navigated, COUNT(*) AS n,
               ROUND(AVG(u.readmit_30d)*100,1) AS readmit_rate_pct,
               ROUND(AVG(u.total_cost_180d),0) AS mean_cost
        FROM navigation_enrollment n
        JOIN patient_encounters p ON p.patient_id = n.patient_id
        JOIN diagnoses d ON d.patient_id = n.patient_id
        JOIN utilization u ON u.patient_id = n.patient_id
        WHERE p.dual_eligible = 1 AND d.cci >= 3
        GROUP BY n.navigated ORDER BY n.navigated
    """,
    "5. Readmission Rate by Comorbidity Burden": """
        SELECT CASE WHEN d.cci=0 THEN '0-None'
                    WHEN d.cci BETWEEN 1 AND 2 THEN '1-2 Mild'
                    WHEN d.cci BETWEEN 3 AND 4 THEN '3-4 Moderate'
                    ELSE '5+ Severe' END AS cci_group,
               n.navigated, COUNT(*) AS n,
               ROUND(AVG(u.readmit_30d)*100,1) AS readmit_rate_pct
        FROM navigation_enrollment n
        JOIN diagnoses d ON d.patient_id = n.patient_id
        JOIN utilization u ON u.patient_id = n.patient_id
        GROUP BY cci_group, n.navigated ORDER BY d.cci, n.navigated
    """,
    "6. Data Quality Check": """
        SELECT 'patient_encounters' AS tbl, COUNT(*) AS rows FROM patient_encounters
        UNION ALL SELECT 'diagnoses', COUNT(*) FROM diagnoses
        UNION ALL SELECT 'utilization', COUNT(*) FROM utilization
        UNION ALL SELECT 'navigation_enrollment', COUNT(*) FROM navigation_enrollment
    """,
}

print("=" * 65)
print("  SQL COHORT ANALYSIS — PATIENT NAVIGATION IMPACT STUDY")
print("=" * 65)

for title, sql in queries.items():
    print(f"\n── {title} ──")
    df = pd.read_sql_query(sql, conn)
    print(df.to_string(index=False))

conn.close()
print("\n" + "=" * 65)
print("  All queries ran successfully against data/claims.db")
print("=" * 65)
